import turtle
import math

def draw_koch(length, depth, inward=True):
    """Draw one Koch-like edge with the 'inward' indentation if inward=True."""
    if depth == 0:
        turtle.forward(length)
        return

    third = length / 3.0
    if inward:
        draw_koch(third, depth - 1, inward)
        turtle.left(60)
        draw_koch(third, depth - 1, inward)
        turtle.right(120)
        draw_koch(third, depth - 1, inward)
        turtle.left(60)
        draw_koch(third, depth - 1, inward)
    else:
        draw_koch(third, depth - 1, inward)
        turtle.right(60)
        draw_koch(third, depth - 1, inward)
        turtle.left(120)
        draw_koch(third, depth - 1, inward)
        turtle.right(60)
        draw_koch(third, depth - 1, inward)

def draw_fractal_polygon(sides, side_length, depth):
    if sides < 3:
        raise ValueError("Number of sides must be at least 3.")

    # Circumradius so the polygon’s side length = side_length
    R = side_length / (2 * math.sin(math.pi / sides))

    # Prepare turtle
    turtle.title(f"{sides}-sided fractal (depth={depth})")
    turtle.speed(12)        # 1 = slowest, 10 = fast, 0 = instant
    turtle.pensize(2)

    # Compute vertices CCW
    offset = math.pi / 2.0
    verts = []
    for i in range(sides):
        theta = offset + 2 * math.pi * i / sides
        x = R * math.cos(theta)
        y = R * math.sin(theta)
        verts.append((x, y))

    # Move to first vertex
    turtle.penup()
    turtle.goto(verts[0])
    turtle.pendown()

    inward = True  # indentations point inward
    for i in range(sides):
        x1, y1 = verts[i]
        x2, y2 = verts[(i + 1) % sides]
        angle_deg = math.degrees(math.atan2(y2 - y1, x2 - x1))
        turtle.setheading(angle_deg)
        draw_koch(side_length, depth, inward)

    turtle.hideturtle()
    turtle.done()

def main():
    sides = int(input("Enter number of sides (>=3): "))
    length = int(input("Enter side length in pixels: "))
    depth = int(input("Enter recursion depth: "))

    draw_fractal_polygon(sides, length, depth)

if __name__ == "__main__":
    main()
