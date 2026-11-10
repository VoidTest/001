// Reconstruction of a small die-cast toy part (barrel / hub with a bolted flange)
// including the two side lugs that held the wheels and had broken off.
//
// All sizes are in millimetres and were ESTIMATED from photos (no scale reference).
// Measure your part with calipers and change the values below, then
// F6 (render) -> File -> Export -> STL in OpenSCAD.
//
// Orientation: tapered "nose" end at z = 0, bolted flange on top (prints this way
// with no supports, except the small axle holes which bridge fine).

/* [Main body] */
body_d        = 17;    // diameter of the cylindrical body
total_h       = 24;    // nose face to top of flange (without bolt heads)
nose_face_d   = 13;    // flat face diameter at the tapered end
nose_h        = 6;     // height of the rounded taper
bore_d        = 6;     // centre hole in the nose face
bore_depth    = 8;

/* [Flange end] */
flange_d      = 20;    // round flange on top
flange_h      = 2.6;
collar_h      = 6;     // squared block under the flange (carries the lugs)
collar_w      = 17.4;  // width across the flats of that block
recess_top_d  = 11;    // cup in the top of the flange
recess_bot_d  = 7;
recess_depth  = 3.5;
bolt_count    = 6;     // 6 bolts, one at "12 o'clock", lugs sit between them
bolt_circle_d = 16.4;
bolt_af       = 1.8;   // hex bolt head across flats
bolt_h        = 0.7;

/* [Wheel lugs - the broken parts] */
lug_w         = 5;     // width of each lug (tangential)
lug_h         = 9;     // height of each lug (along body axis)
lug_reach     = 12.5;  // distance from axis to the outer lug face
axle_style    = "hole"; // [hole, pin, none]
axle_d        = 2.0;   // hole diameter (use 2.1 for a 2 mm steel axle) or pin diameter
axle_depth    = 6;     // hole depth into each lug, or pin length out of it
axle_z_from_top = 4.5; // axle centre measured down from flange top

/* [Details] */
hex_af        = 4;     // hex recess on the side
hex_depth     = 2.5;
hex_z         = 12;
mark_d        = 2.2;   // the two small circles on the nose face
mark_offset   = 4.6;

$fn = 96;
eps = 0.01;

flange_z = total_h - flange_h;
collar_z = flange_z - collar_h;
lug_z    = total_h - lug_h;
axle_z   = total_h - axle_z_from_top;

module nose_profile() {
    // 2D half-profile for rotate_extrude: rounded shoulder from nose face to body
    steps = 24;
    pts = concat(
        [[0, 0]],
        [for (i = [0:steps]) let(t = i / steps)
            [nose_face_d/2 + (body_d - nose_face_d)/2 * sin(t * 90), nose_h * (1 - cos(t * 90)) ]],
        [[body_d/2, collar_z + eps], [0, collar_z + eps]]);
    polygon(pts);
}

module collar() {
    // squared block with chamfered bottom edges (the "arrow" shapes seen on the flats)
    ch = 2;
    translate([0, 0, collar_z])
    intersection() {
        cylinder(d = flange_d - 0.4, h = collar_h + eps);
        hull() {
            translate([-collar_w/2, -collar_w/2, ch]) cube([collar_w, collar_w, collar_h - ch + eps]);
            translate([-body_d/2 + 0.2, -body_d/2 + 0.2, 0]) cube([body_d - 0.4, body_d - 0.4, eps]);
        }
    }
}

module flange() {
    translate([0, 0, flange_z]) {
        cylinder(d = flange_d, h = flange_h);
        for (i = [0:bolt_count-1])
            rotate(i * 360 / bolt_count + 90)
                translate([bolt_circle_d/2, 0, flange_h - eps]) {
                    cylinder(d = bolt_af * 1.35, h = 0.2);                       // washer
                    cylinder(d = bolt_af / cos(30), h = bolt_h, $fn = 6);       // hex head
                    translate([0, 0, bolt_h - eps])
                        cylinder(d1 = bolt_af * 0.9, d2 = bolt_af * 0.5, h = 0.25); // domed top
                }
    }
}

module lugs() {
    for (s = [-1, 1]) mirror([s < 0 ? 1 : 0, 0, 0]) {
        translate([0, -lug_w/2, lug_z]) cube([lug_reach, lug_w, lug_h]);
        if (axle_style == "pin")
            translate([lug_reach - eps, 0, axle_z]) rotate([0, 90, 0])
                cylinder(d = axle_d, h = axle_depth);
    }
}

module axle_holes() {
    if (axle_style == "hole")
        for (s = [-1, 1]) mirror([s < 0 ? 1 : 0, 0, 0])
            translate([lug_reach - axle_depth, 0, axle_z]) rotate([0, 90, 0])
                cylinder(d = axle_d, h = axle_depth + 1, $fn = 32);
}

module hub() {
    difference() {
        union() {
            rotate_extrude() nose_profile();
            collar();
            flange();
            lugs();
        }
        // cup in the flange
        translate([0, 0, total_h - recess_depth])
            cylinder(d1 = recess_bot_d, d2 = recess_top_d, h = recess_depth + eps);
        translate([0, 0, total_h - recess_depth - 0.4])
            cylinder(d = recess_bot_d - 1.2, h = 0.4 + eps);
        // small groove just under the flange
        translate([0, 0, flange_z - 0.35])
            difference() { cylinder(d = flange_d + 1, h = 0.35); cylinder(d = flange_d - 1.2, h = 0.35); }
        // centre bore in the nose
        translate([0, 0, -eps]) cylinder(d = bore_d, h = bore_depth);
        // two marks on the nose face: filled dot and engraved ring
        translate([0,  mark_offset, -eps]) cylinder(d = mark_d, h = 0.5, $fn = 32);
        translate([0, -mark_offset, -eps]) difference() {
            cylinder(d = mark_d + 0.2, h = 0.3, $fn = 32);
            cylinder(d = mark_d - 0.3, h = 0.3, $fn = 32);
        }
        // hex recess on the side
        translate([0, body_d/2 - hex_depth, hex_z]) rotate([-90, 0, 0])
            cylinder(d = hex_af / cos(30), h = hex_depth + 2, $fn = 6);
        translate([0, body_d/2 - hex_depth - 2, hex_z]) rotate([-90, 0, 0])
            cylinder(d = hex_af * 0.55, h = 3, $fn = 32);
        axle_holes();
    }
}

hub();
