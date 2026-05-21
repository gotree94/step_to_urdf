import FreeCAD, Part, Mesh

doc = FreeCAD.newDocument("test")
part = doc.addObject("Part::Box", "Box")
part.Length = 10
part.Width = 10
part.Height = 10
doc.recompute()

mesh = Mesh.Mesh(part.Shape.tessellate(0.1))
mesh.write("C:\Users\user\Desktop\URDFly\output\test.stl")
print("OK: test.stl created")
FreeCAD.closeDocument("test")
