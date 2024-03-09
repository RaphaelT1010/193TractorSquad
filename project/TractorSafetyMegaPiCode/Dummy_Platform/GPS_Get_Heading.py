
def pivotCCW(heading):
    print(f"Turning counter clockwise by {heading} degrees")

def pivotCW(heading):
    print(f"Turning clockwise by {heading} degrees")


def testheading(destHeading, currentHeading):
    resultheading = destHeading - currentHeading
    adj_heading = 360 - abs(resultheading)

    if adj_heading < 180:
        heading = adj_heading
        if resultheading < 0:
            pivotCW(abs(heading))
        else:
            pivotCCW(abs(heading))

    else: 
        heading = resultheading
        if resultheading < 0:
            pivotCCW(abs(heading))
        else:
            pivotCW(abs(heading))

# testheading(45, 190)