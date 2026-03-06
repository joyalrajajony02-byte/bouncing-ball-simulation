# scene.py - Build USD scene with multiple bouncing balls,
# shadows, and color changes on bounce

from pxr import Usd, UsdGeom, UsdLux, Gf, Vt, Sdf
import config


def get_bounce_color(bounce_count):
    """Pick a color based on how many times the ball bounced."""
    colors = config.BALL_COLORS
    idx = bounce_count % len(colors)
    c = colors[idx]
    return Gf.Vec3f(c[0], c[1], c[2])


def create_scene(usd_path, all_positions, all_bounces):
    """Create animated USD with multiple balls, shadows, and color changes."""
    stage = Usd.Stage.CreateNew(usd_path)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
    stage.SetStartTimeCode(0)
    stage.SetEndTimeCode(len(all_positions) - 1)
    stage.SetFramesPerSecond(config.FPS)

    n = config.NUM_BALLS
    s = config.FLOOR_SIZE

    # --- Floor ---
    floor = UsdGeom.Mesh.Define(stage, "/World/Floor")
    floor.GetPointsAttr().Set(Vt.Vec3fArray([
        Gf.Vec3f(-s, 0, -s), Gf.Vec3f(s, 0, -s),
        Gf.Vec3f(s, 0, s), Gf.Vec3f(-s, 0, s),
    ]))
    floor.GetFaceVertexCountsAttr().Set(Vt.IntArray([4]))
    floor.GetFaceVertexIndicesAttr().Set(Vt.IntArray([0, 1, 2, 3]))
    fc = config.FLOOR_COLOR
    floor.GetDisplayColorAttr().Set(
        Vt.Vec3fArray([Gf.Vec3f(fc[0], fc[1], fc[2])]))

    # --- Create balls and shadows ---
    ball_xforms = []
    ball_shapes = []
    ball_color_pvs = []
    shadow_xforms = []
    shadow_shapes = []

    for i in range(n):
        # Ball
        bx = UsdGeom.Xform.Define(stage, f"/World/Ball_{i}")
        bs = UsdGeom.Sphere.Define(stage, f"/World/Ball_{i}/Shape")
        bs.GetRadiusAttr().Set(config.BALL_RADIUS)

        # Ball color (per-frame, so use primvar)
        cpv = UsdGeom.PrimvarsAPI(bs).CreatePrimvar(
            "displayColor", Sdf.ValueTypeNames.Color3fArray,
            UsdGeom.Tokens.constant
        )

        ball_xforms.append(bx)
        ball_shapes.append(bs)
        ball_color_pvs.append(cpv)

        # Shadow (flat dark circle on the floor)
        sx = UsdGeom.Xform.Define(stage, f"/World/Shadow_{i}")
        sc = UsdGeom.Cylinder.Define(stage, f"/World/Shadow_{i}/Shape")
        sc.GetRadiusAttr().Set(config.BALL_RADIUS * 0.8)
        sc.GetHeightAttr().Set(0.005)
        sc.GetAxisAttr().Set("Y")
        sc.GetDisplayColorAttr().Set(
            Vt.Vec3fArray([Gf.Vec3f(0.1, 0.1, 0.1)]))
        sc.GetDisplayOpacityAttr().Set(Vt.FloatArray([0.5]))

        shadow_xforms.append(sx)
        shadow_shapes.append(sc)

    # --- Animate each frame ---
    print(f"Writing {len(all_positions)} frames to USD...")
    for frame in range(len(all_positions)):
        for i in range(n):
            pos = all_positions[frame][i]
            bounces = all_bounces[frame][i]

            # Move ball
            ball_xforms[i].ClearXformOpOrder()
            op = ball_xforms[i].AddTranslateOp()
            op.Set(Gf.Vec3d(pos[0], pos[1], pos[2]), time=frame)

            # Change color based on bounce count
            color = get_bounce_color(bounces)
            ball_color_pvs[i].Set(Vt.Vec3fArray([color]), time=frame)

            # Move shadow (stays on floor under the ball)
            shadow_xforms[i].ClearXformOpOrder()
            sop = shadow_xforms[i].AddTranslateOp()
            sop.Set(Gf.Vec3d(pos[0], 0.003, pos[2]), time=frame)

            # Shadow size: smaller when ball is higher
            height = max(pos[1], 0.1)
            scale_factor = max(0.3, 1.0 / (1.0 + height * 0.3))
            shadow_xforms[i].ClearXformOpOrder()
            sop2 = shadow_xforms[i].AddTranslateOp()
            sop2.Set(Gf.Vec3d(pos[0], 0.003, pos[2]), time=frame)
            ssc = shadow_xforms[i].AddScaleOp()
            ssc.Set(Gf.Vec3d(scale_factor, 1.0, scale_factor), time=frame)

    # --- Light ---
    light = UsdLux.DistantLight.Define(stage, "/World/Light")
    light.CreateIntensityAttr().Set(5000)

    stage.GetRootLayer().Save()
    print(f"Saved: {usd_path}")
