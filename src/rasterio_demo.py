import rasterio
import rasterio.mask
from rasterio.plot import show
import shapely.geometry
from geojson import Polygon, Feature
from matplotlib import pyplot as plt


src = rasterio.open("/home/gnampfelix/repositories/github.com/jufischi/Group-Project-Sequence/data/NE1_50M_SR_W.tif")
# Some arbitrary definition of "europe" using lat/long
europe = [(43.9, -1.0), (54.7, 23.5)]
europe_x = [e[1] for e in europe]
europe_y = [e[0] for e in europe]

airport_stuttgart = (48.7, 9.2)
airport_munich = (48.4, 11.8)
airports = [airport_stuttgart, airport_munich]

print("DEMO: Mark Europe on map using transforms")
# # Transform Long/Lat in pixel coordinates and build a shape
# rows, cols = rasterio.transform.rowcol(src.transform, europe_x, europe_y)
# europe_shape = shapely.geometry.box(cols[0], rows[0], cols[1], rows[1])

# f, ax = plt.subplots()
# plt.imshow(src.read(1))
# ax.plot(*europe_shape.exterior.xy)
# plt.show()

print("DEMO: Mark Europe on map using extent")
# europe_shape = shapely.geometry.box(europe_x[0], europe_y[0], europe_x[1], europe_y[1])
# extend = [src.bounds[0], src.bounds[2], src.bounds[1], src.bounds[3]]
# f, ax = plt.subplots()
# ax.imshow(src.read(1), extent=extend)
# ax.plot(*europe_shape.exterior.xy)
# plt.show()

print("DEMO: Show only europe")
# europe_shape = shapely.geometry.box(europe_x[0], europe_y[0], europe_x[1], europe_y[1])
# out_image, out_transform = rasterio.mask.mask(src, [europe_shape], crop=True)
# show(out_image)

print("DEMO: Show only europe, highlight airport")
# europe_shape = shapely.geometry.box(europe_x[0], europe_y[0], europe_x[1], europe_y[1])
# out_image, out_transform = rasterio.mask.mask(src, [europe_shape], crop=True)
# y, x = rasterio.transform.rowcol(out_transform, [e[1] for e in airports], [e[0] for e in airports])

# f, ax = plt.subplots()
# show(out_image, ax=ax)
# ax.scatter(x, y)
# plt.show()

print("DEMO: Show only europe, highlight airport connection")
europe_shape = shapely.geometry.box(europe_x[0], europe_y[0], europe_x[1], europe_y[1])
out_image, out_transform = rasterio.mask.mask(src, [europe_shape], crop=True)
y, x = rasterio.transform.rowcol(out_transform, [e[1] for e in airports], [e[0] for e in airports])

f, ax = plt.subplots()
show(out_image, ax=ax)
ax.plot(x, y, c="red", linestyle="-.", marker = "o")
plt.axis("off")
plt.show()


#show(src.read(1), extent=extend, ax=ax)
# shape = shapely.geometry.box(20, 20, 40, 40)
#out_image, out_transform = rasterio.mask.mask(src, [europe_shape], crop=True)
#show(out_image)
#extend = [src.bounds[0], src.bounds[2], src.bounds[1], src.bounds[3]]

