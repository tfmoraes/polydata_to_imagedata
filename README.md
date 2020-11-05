# PolyData to ImageData

This code is used to voxelize a mesh (vtkPolyData). I can be called this way in shell:

```shell
python3 polydata_to_imagedata.py mesh_file  output_file.vti
```

`mesh_file` is a STL or PLY file. `output_file.vti` is vtkImageData file that can be opened in Paraview.

It's also possible to `import polydata_to_imagedata` in a **Python** script and use the function `polydata_to_imagedata` to convert a vtkPolyData to a vtkImageData.
