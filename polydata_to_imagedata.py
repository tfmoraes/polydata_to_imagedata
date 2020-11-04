import math
import sys

import vtk


def read_mesh_file(filename):
    if filename.lower().endswith(".stl"):
        reader = vtk.vtkSTLReader()
    elif filename.lower().endswith(".ply"):
        reader = vtk.vtkPLYReader()
    else:
        raise ValueError("Only reads STL and PLY")
    reader.SetFileName(filename)
    reader.Update()
    return reader.GetOutput()


def polydata_to_imagedata(polydata, dimensions=(100, 100, 100), padding=0):
    xi, xf, yi, yf, zi, zf = polydata.GetBounds()
    dx, dy, dz = dimensions

    # Calculating spacing
    sx = (xf - xi) / dx
    sy = (yf - yi) / dy
    sz = (zf - zi) / dz

    # Calculating Origin
    ox = xi + sx / 2.0
    oy = yi + sy / 2.0
    oz = zi + sz / 2.0

    if padding:
        ox -= sx
        oy -= sy
        oz -= sz

        dx += 2 * padding
        dy += 2 * padding
        dz += 2 * padding

    image = vtk.vtkImageData()
    image.SetSpacing((sx, sy, sz))
    image.SetDimensions((dx, dy, dz))
    image.SetExtent(0, dx - 1, 0, dy - 1, 0, dz - 1)
    image.SetOrigin((ox, oy, oz))
    image.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1)

    inval = 255
    outval = 0

    for i in range(image.GetNumberOfPoints()):
        image.GetPointData().GetScalars().SetTuple1(i, inval)

    pol2stenc = vtk.vtkPolyDataToImageStencil()
    pol2stenc.SetInputData(polydata)
    pol2stenc.SetOutputOrigin((ox, oy, oz))
    pol2stenc.SetOutputSpacing((sx, sy, sz))
    pol2stenc.SetOutputWholeExtent(image.GetExtent())
    pol2stenc.Update()

    imgstenc = vtk.vtkImageStencil()
    imgstenc.SetInputData(image)
    imgstenc.SetStencilConnection(pol2stenc.GetOutputPort())
    imgstenc.ReverseStencilOff()
    imgstenc.SetBackgroundValue(outval)
    imgstenc.Update()

    return imgstenc.GetOutput()


def save(imagedata, filename):
    writer = vtk.vtkXMLImageDataWriter()
    writer.SetFileName(filename)
    writer.SetInputData(imagedata)
    writer.Write()


def main():
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    polydata = read_mesh_file(input_filename)
    imagedata = polydata_to_imagedata(polydata)
    save(imagedata, output_filename)


if __name__ == "__main__":
    main()
