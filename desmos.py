from svgpathtools import Line, CubicBezier, svg2paths


paths,attributes = svg2paths('assets/hinata_edges.svg')

with open('instructions.txt','w') as f:
    for i,path in enumerate(paths):
        for segment in path:
            if isinstance(segment,Line):
                x1, y1 = segment.start.real, segment.start.imag
                x2, y2 = segment.end.real, segment.end.imag
                m = (y2 - y1) / max((x2 - x1),0.0001)
                b = y1 - m * x1
                slope_threshold = 1
                if abs(m) <= slope_threshold:
                    domain_min = min(x1, x2)
                    domain_max = max(x1, x2)
                    f.write(
                        f'y = {m}x + {b} \\left\\{{ {domain_min:.2f} \\leq x \\leq {domain_max:.2f} \\right\\}} \n'
                    )
                else:
                    if m == float('inf'):
                        f.write(
                            f'x = {x1:.2f} \\left\\{{ {min(y1, y2):.2f} \\leq y \\leq {max(y1, y2):.2f} \\right\\}} \n'
                        )
            elif isinstance(segment, CubicBezier):
                x0, y0 = segment.start.real, segment.start.imag
                x1, y1 = segment.control1.real, segment.control1.imag
                x2, y2 = segment.control2.real, segment.control2.imag
                x3, y3 = segment.end.real, segment.end.imag
                
                x_expr = (
                    f"(1 - t)^3*{x0:.1f} + "
                    f"3*t*(1 - t)^2*{x1:.1f} + "
                    f"3*t^2*(1 - t)*{x2:.1f} + "
                    f"t^3*{x3:.1f}"
                )
                y_expr = (
                    f"(1 - t)^3*{y0:.1f} + "
                    f"3*t*(1 - t)^2*{y1:.1f} + "
                    f"3*t^2*(1 - t)*{y2:.1f} + "
                    f"t^3*{y3:.1f}"
                )

                f.write(f'\\left({x_expr},{y_expr}\\right)\n')