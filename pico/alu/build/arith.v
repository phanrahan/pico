module Invert2 (input [1:0] I, output [1:0] O);
wire  inst0_O;
wire  inst1_O;
SB_LUT4 #(.LUT_INIT(16'h5555)) inst0 (.I0(I[0]), .I1(1'b0), .I2(1'b0), .I3(1'b0), .O(inst0_O));
SB_LUT4 #(.LUT_INIT(16'h5555)) inst1 (.I0(I[1]), .I1(1'b0), .I2(1'b0), .I3(1'b0), .O(inst1_O));
assign O = {inst1_O,inst0_O};
endmodule

module Mux2x2 (input [1:0] I0, input [1:0] I1, input  S, output [1:0] O);
wire  inst0_O;
wire  inst1_O;
SB_LUT4 #(.LUT_INIT(16'hCACA)) inst0 (.I0(I0[0]), .I1(I1[0]), .I2(S), .I3(1'b0), .O(inst0_O));
SB_LUT4 #(.LUT_INIT(16'hCACA)) inst1 (.I0(I0[1]), .I1(I1[1]), .I2(S), .I3(1'b0), .O(inst1_O));
assign O = {inst1_O,inst0_O};
endmodule

module Adc2 (input [1:0] I0, input [1:0] I1, input  CIN, output [1:0] O, output  COUT);
wire  inst0_O;
wire  inst1_CO;
wire  inst2_O;
wire  inst3_CO;
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst0 (.I0(1'b0), .I1(I0[0]), .I2(I1[0]), .I3(CIN), .O(inst0_O));
SB_CARRY inst1 (.I0(I0[0]), .I1(I1[0]), .CI(CIN), .CO(inst1_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst2 (.I0(1'b0), .I1(I0[1]), .I2(I1[1]), .I3(inst1_CO), .O(inst2_O));
SB_CARRY inst3 (.I0(I0[1]), .I1(I1[1]), .CI(inst1_CO), .CO(inst3_CO));
assign O = {inst2_O,inst0_O};
assign COUT = inst3_CO;
endmodule

module main (input [6:0] J1, output [2:0] J3, input  CLKIN);
wire [1:0] inst0_O;
wire [1:0] inst1_O;
wire [1:0] inst2_O;
wire  inst2_COUT;
wire  inst3_O;
Invert2 inst0 (.I({J1[3],J1[2]}), .O(inst0_O));
Mux2x2 inst1 (.I0({J1[3],J1[2]}), .I1(inst0_O), .S(J1[5]), .O(inst1_O));
Adc2 inst2 (.I0({J1[1],J1[0]}), .I1(inst1_O), .CIN(inst3_O), .O(inst2_O), .COUT(inst2_COUT));
SB_LUT4 #(.LUT_INIT(16'h6C6C)) inst3 (.I0(J1[4]), .I1(J1[5]), .I2(J1[6]), .I3(1'b0), .O(inst3_O));
assign J3 = {inst2_COUT,inst2_O[1],inst2_O[0]};
endmodule

