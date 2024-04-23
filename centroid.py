

def polygon_centroid(vertices):
    n = len(vertices)
    area = 0
    centroid_x = 0
    centroid_y = 0

    for i in range(n):
        j = (i + 1) % n
        cross_product = (vertices[i][0] * vertices[j][1]) - (vertices[j][0] * vertices[i][1])
        area += cross_product
        centroid_x += (vertices[i][0] + vertices[j][0]) * cross_product
        centroid_y += (vertices[i][1] + vertices[j][1]) * cross_product

    area /= 2
    centroid_x /= (6 * area)
    centroid_y /= (6 * area)

    return centroid_x, centroid_y

# Example usage:
vertices = [(56.8233333,4.3466667),(57.0933333,5.1680556),(56.7380556,5.4975),(56.5916667,5.0336111),(56.4838889,4.6413889)]  # Example square vertices
centroid = polygon_centroid(vertices)
print("Centroid:", centroid)