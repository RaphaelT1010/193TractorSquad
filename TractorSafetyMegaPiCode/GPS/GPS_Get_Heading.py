
def pivotCCW(heading):
    print(f"Turning counter clockwise by {heading} degrees")

def pivotCW(heading):
    print(f"Turning counter clockwise by {heading} degrees")


def testheading(destHeading, currentHeading):
    resultheading = destHeading - currentHeading
    heading = 360 - abs(resultheading)

    if heading > 180:
        heading = resultheading

    if resultheading < 0:
        pivotCCW(abs(heading))
    else:
        pivotCW(abs(heading))

testheading(0, 0)