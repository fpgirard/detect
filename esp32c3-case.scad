// Pascal Girard 2022

$fn = 40;

/* [Case Dimensions] */
case_iw = 26;        // inner height
case_il = 34.5;      // inner length
case_ih = 9;        // inner height
case_wall = 1.5;
sensor_base = 13;    // pad for temp/humidity sensor

/* [Foot Dimensions] */
foot_base = 6;
foot_height = 1.3;
foot_width = 20;
radius =  1;

/* [Opening Dimensions] */
usb_d = 4; 
usb_width = 6;
usb_height = case_wall + foot_height + 1.5;
i2_height = 5.5;
reset_d = 2;
reset_width = 2;
reset_height = case_wall + foot_height + .5;

post_h = 6.4;

module mirror2(v) {
    children();
    mirror(v) children();
}

module feet() {
    module foot() {
        translate([(case_il-foot_base)/2,0, foot_height]) {    
            cube([foot_base,foot_width,foot_height], center = true);   // foot base
            }
        }
    mirror2([1,0,0]) translate([(-(case_il-foot_base)), 0, 0])foot();
}
        
module case () {
     module reset_hole() {
         rotate([0,90,90]) {
            hull() {
                cylinder(h = case_wall * 2, d = reset_d, center=true);
                translate([0,reset_width,0]) cylinder(h = case_wall * 2, d = reset_d, center=true);
            }
         }
    }
    difference() {
            difference () {
                hull() {
                    for ( i = [-1,1] ) {
                        for (j=[-1,1]) {
                            translate([i*(case_il + case_wall)/2,j*(case_iw + case_wall)/2,0]) {
                                cylinder(case_ih, d = case_wall, true);
                            }
                        }
                    }
                } 
                translate([0,0,case_ih/2+case_wall]) {        // create a floor
                    cube([case_il, case_iw, case_ih], center = true);
                }
            }
        translate ([case_il/2, -3.25, usb_height]) {     // usb hole
            rotate([0,90,0]) {
                hull() {
                    cylinder(h = case_wall * 2, d = usb_d, center=true);
                    translate([0,usb_width,0]) 
                        cylinder(h = case_wall * 2, d = usb_d, center=true);
                }
            }
        }
        // reset & pin 0 holes
            mirror2 ([0,1,0]) translate ([(case_il-6)/2, -case_iw/2, reset_height]) { reset_hole(); }
    }
}

module cover() {
    difference() {
        hull() {
            for ( i = [-1,1] ) {
            for (j=[-1,1]) {
                translate([i*(case_il + case_wall)/2,j*(case_iw + case_wall)/2,0]) {
                    cylinder(case_wall, d = case_wall, true);
                    }
                }
            }
            
        }
        translate([-case_il/2 - case_wall,-(case_iw-sensor_base)/2,0])cube([case_wall,sensor_base,case_wall]);

    }
    union() {
        for ( i = [-1,1] ) {
            for (j=[-1,1]) {
                // posts
                translate([i*(case_il - 2*case_wall)/2,j*(case_iw - 2*case_wall)/2,5-case_wall]) {
                    cube([2*case_wall, 2*case_wall, 5],true);
            
                }
            }
        }    
    }
}    
translate([0,20,0]) cover();
translate([0,-20,0]) {case();feet();}
