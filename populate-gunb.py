from mps_config import MPSConfig, models
from sqlalchemy import MetaData
#The MPSConfig object points to our database file.
conf = MPSConfig()

#Clear everything out of the database.
conf.clear_all()

#session is a connection to that database.
session = conf.session

#First lets define our mitigation devices.
shutter = models.MitigationDevice(name="Shutter")
aom = models.MitigationDevice(name="AOM")
session.add_all([shutter, aom])

#Make some beam classes.
class_0 = models.BeamClass(number=0,name="Power Class 0",description="No Beam")
class_1 = models.BeamClass(number=1,name="Power Class 1",description="YAG Max Power")
class_2 = models.BeamClass(number=2,name="Power Class 2",description="Full Power")
session.add_all([class_0, class_1, class_2])

# EIC Link Node - L2KA00-05 (Level 17)
# Make a crate for BPMs, and for the mitigation LN
crate = models.Crate(number=1, shelf_number=1, num_slots=8)
session.add_all([crate])

#Define a mixed-mode link node (One digital AMC, one analog for IM01/SOL01-02 Curr/Faraday Cup Curr)
eic_link_node_type = models.ApplicationType(name="EIC Link Node", number=0,
                                            digital_channel_count=9, digital_channel_size=1,
                                            analog_channel_count=4, analog_channel_size=1)
bpm_app_type = models.ApplicationType(name="BPM Card", number=1,
                                      digital_channel_count=0, digital_channel_size=1,
                                      analog_channel_count=2, analog_channel_size=1)
bcm_app_type = models.ApplicationType(name="BCM Card", number=2,
                                      digital_channel_count=0, digital_channel_size=1,
                                      analog_channel_count=2, analog_channel_size=1)


session.add_all([eic_link_node_type])

# Applications - an application is basically an analog or digital status
# summary embedded in a link node message, which contains status from
# all inputs connected to it (coming from wires or from the backplane)
eic_digital_app = models.Application(global_id=0, name="EIC_Digital", description="EIC Digital Status")
bpm_eic_app = models.Application(global_id=1,name="EIC_BPM",description="EIC BPM Status")
toro_sol_app = models.Application(global_id=2,name="EIC_Analog",description="IM01/SOL1/SOL2/FC Status")
session.add_all([eic_digital_app, bpm_eic_app, toro_sol_app])

#Install a mixed-mode link node card in the crate.
link_node_card = models.ApplicationCard(number=1, type=eic_link_node_type, slot_number=2)
bpm_card = models.ApplicationCard(number=2, type=bpm_app_type, slot_number=3)
toroid_card = models.ApplicationCard(number=2, type=bcm_app_type, slot_number=6)
fc_card = models.ApplicationCard(number=2, type=bcm_app_type, slot_number=7)
crate.cards.append(link_node_card)
crate.cards.append(bpm_card)
crate.cards.append(toroid_card)
crate.cards.append(fc_card)
session.add_all([link_node_card,bpm_card,toroid_card,fc_card])

#Define some channels for the card.
# channel 0 - YAG01 out switch
# channel 1 - YAG01 in switch
# channel 2 - Gun temperature
# channel 3 - Waveguide temperature
# channel 4 - Buncher temperature
# channel 5 - SOL01 temperature
# channel 6 - SOL02 temperature
# channel 7 - VVR01 vacuum status
# channel 8 - VVR02 vacuum status
digital_chans = []

names=[]
#===========  device, zero name, one name, fault state
names.append(("YAG01_OUT_SWITCH", "IS_OUT", "NOT_OUT", 1))
names.append(("YAG01_IN_SWITCH", "IS_IN", "NOT_IN", 1))
names.append(("GUN_TEMP", "IS_FAULTED", "IS_OK", 0))
names.append(("WAVEGUIDE_TEMP", "IS_FAULTED", "IS_OK", 0))
names.append(("BUNCHER_TEMP", "IS_FAULTED", "IS_OK", 0))
names.append(("SOL01_TEMP", "IS_FAULTED", "IS_OK", 0))
names.append(("SOL02_TEMP", "IS_FAULTED", "IS_OK", 0))
names.append(("VVR01_VAC", "IS_FAULTED", "IS_OK", 0))
names.append(("VVR02_VAC", "IS_FAULTED", "IS_OK", 0))

for i in range(0,9):
  chan = models.DigitalChannel(number=i)
  (name, z_name, o_name, alarm_state) = names[i]
  chan.name = name
  chan.z_name = z_name
  chan.o_name = o_name
  chan.alarm_state = alarm_state
  chan.card = link_node_card
  digital_chans.append(chan)
  session.add(chan)

# LN card analog channels
# channel 0 - SOL01 Current
# channel 1 - SOL02 Current
#im01_channel = models.AnalogChannel(name="IM01 Charge", number=0, card = link_node_card)
#fc_channel = models.AnalogChannel(name="Faraday Cup Current", number=1, card = link_node_card)
#sol01_channel = models.AnalogChannel(name="SOL01 Current", number=2, card = link_node_card)
#sol02_channel = models.AnalogChannel(name="SOL02 Current", number=3, card = link_node_card)
bpm01_channel = models.AnalogChannel(name="BPM01", number=0, card = bpm_card)
bpm02_channel = models.AnalogChannel(name="BPM02", number=1, card = bpm_card)
# channel 0 - IM01
# channel 1 - Faraday Cup (FC)

session.add_all([bpm01_channel, bpm02_channel])

# Add digital device types
profmon_device_type = models.DeviceType(name="Profile Monitor")
temp_device_type = models.DeviceType(name="Temperature")
vvr_device_type = models.DeviceType(name="Vacuum Status")
session.add_all([profmon_device_type, temp_device_type, vvr_device_type])

# Add analog device types
#im_device_type = models.AnalogDeviceType(name="ICT", units="uC")
#fc_device_type = models.AnalogDeviceType(name="Faraday Cup", units="mA")
#sol_curr_device_type = models.AnalogDeviceType(name="Solenoid Curretn", units="mA")
#session.add_all([im_device_type, fc_device_type, sol_curr_device_type])

# New analog devices
bpm_device_type = models.DeviceType(name="BPM")
session.add_all([bpm_device_type])

#generic_threshold_map = models.ThresholdValueMap(description="Generic threshold map for analog devices")
#for i in range(0,15):
#  threshold = models.ThresholdValue(threshold=i, value=0.25*i)
#  generic_threshold_map.values.append(threshold)
#session.add(generic_threshold_map)

#fc_threshold_map = models.ThresholdValueMap(description="Mapping for Faraday Cup Threshold")
#fc_threshold_ok = models.ThresholdValue(threshold=0, value=0.05)
#fc_threshold_map.values.append(fc_threshold_ok)
#fc_threshold = models.ThresholdValue(threshold=1, value=0.1)
#fc_threshold_map.values.append(fc_threshold)
#session.add(fc_threshold_map)

#sol_threshold_map = models.ThresholdValueMap(description="Mapping for Solenoid Current Threshold")
#sol_threshold = models.ThresholdValue(threshold=0, value=0.05)
#sol_threshold_map.values.append(sol_threshold)
#session.add(sol_threshold_map)

#im_device_type.threshold_value_map = generic_threshold_map
#fc_device_type.threshold_value_map = fc_threshold_map
#sol_curr_device_type.threshold_value_map = sol_threshold_map

# Define some states for the device types
screen_out        = models.DeviceState(name="Out", device_type = profmon_device_type, value = 2)
screen_in         = models.DeviceState(name="In", device_type = profmon_device_type, value = 1)
screen_moving     = models.DeviceState(name="Moving", device_type = profmon_device_type, value = 3)
screen_broken     = models.DeviceState(name="Broken", device_type = profmon_device_type, value = 0)
temp_device_fault = models.DeviceState(name="Temp Fault", device_type = temp_device_type, value = 0)
temp_device_ok    = models.DeviceState(name="Temp OK", device_type = temp_device_type, value = 1)
vvr_device_fault  = models.DeviceState(name="Vacuum Fault", device_type = vvr_device_type, value = 0)
vvr_device_ok     = models.DeviceState(name="Vacuum OK", device_type = vvr_device_type, value = 1)
session.add_all([screen_out, screen_in, screen_moving, screen_broken,
                 temp_device_fault, temp_device_ok,
                 vvr_device_fault, vvr_device_ok])

#
# BPM DeviceStates - Threshold States
#
# There are 8 comparators for each X, Y and TMIT. Each comparator checks if
# the measurement in within the low and high thresholds. If a bit is set
# it means the measured value is outside the low/high window.
#
bpm_states=[]
state_value = 1
# X Thresholds - bits 0 through 7
for i in range(0,8):
  state_name = "X_THRSLD" + str(i)
  bpm_threshold_state = models.DeviceState(name=state_name, value=state_value, mask=state_value, device_type = bpm_device_type)
  bpm_states.append(bpm_threshold_state)
  session.add(bpm_threshold_state)
  state_value = (state_value << 1)
# Y Thresholds - bits 8 through 15
for i in range(0,8):
  state_name = "Y_THRSLD" + str(i)
  bpm_threshold_state = models.DeviceState(name=state_name, value=state_value, mask=state_value, device_type = bpm_device_type)
  bpm_states.append(bpm_threshold_state)
  session.add(bpm_threshold_state)
  state_value = (state_value << 1)
# TMIT Thresholds - bits 16 though 23
for i in range(0,8):
  state_name = "T_THRSLD" + str(i)
  bpm_threshold_state = models.DeviceState(name=state_name, value=state_value, mask=state_value, device_type = bpm_device_type)
  bpm_states.append(bpm_threshold_state)
  session.add(bpm_threshold_state)
  state_value = (state_value << 1)

session.commit()

#Add digital devices
screen = models.DigitalDevice(name="YAG01", z_position=-28.061394, description="YAG Screen",
                              device_type = profmon_device_type, application = eic_digital_app)
gun_temp = models.DigitalDevice(name="Gun Temperature", device_type = temp_device_type,
                                application = eic_digital_app, z_position = 0,
                                description = "Gun Temperature Summary Input")
wg_temp = models.DigitalDevice(name="Waveguide Temperature", device_type = temp_device_type, 
                               application = eic_digital_app, z_position = 0,
                               description = "Waveguide Temperature Summary Input")
buncher_temp = models.DigitalDevice(name="Buncher Temperature", device_type = temp_device_type,
                                    application = eic_digital_app, z_position = -30.299721,
                                    description = "Buncher Temperature Summary Input")
sol01_temp = models.DigitalDevice(name="SOL01 Temp", z_position=-32.115049, description="SOL01 Temperature",
                                  device_type = temp_device_type, application = eic_digital_app)
sol02_temp = models.DigitalDevice(name="SOL02 Temp", z_position=-27.538278, description="SOL02 Temperature",
                                  device_type = temp_device_type, application = eic_digital_app)
vvr1 = models.DigitalDevice(name="VVR01", z_position=-31, description="Vacuum Gate Valve VVR01",
                                  device_type = vvr_device_type, application = eic_digital_app)
vvr2 = models.DigitalDevice(name="VVR02", z_position=-26, description="Vacuum Gate Valve VVR02",
                                  device_type = vvr_device_type, application = eic_digital_app)

session.add_all([screen, gun_temp, wg_temp, buncher_temp,
                 sol01_temp, sol02_temp, vvr1, vvr2])

# Add analog devices
#im01 = models.AnalogDevice(name="IM01", analog_device_type=im_device_type, channel=im01_channel,
#                           application=global_app, z_position=-31.00474, description="ICT Charge")
#fc = models.AnalogDevice(name="FC", analog_device_type=im_device_type, channel=fc_channel,
#                           application=global_app, z_position=-25, description="Faraday Cup Current")
#sol01_curr = models.AnalogDevice(name="SOL01", analog_device_type=im_device_type, channel=sol01_channel,
#                                 application=global_app, z_position=-32.115049, description="SOL01 Current")
#sol02_curr = models.AnalogDevice(name="SOL02", analog_device_type=im_device_type, channel=sol02_channel,
#                                 application=global_app, z_position=-27.538278, description="SOL02 Current")
bpm01 = models.AnalogDevice(name="BPM01", device_type = bpm_device_type, channel=bpm01_channel,
                            application=bpm_eic_app, z_position=-31.349744, description="BPM01")
bpm02 = models.AnalogDevice(name="BPM02", device_type = bpm_device_type, channel=bpm02_channel,
                            application=bpm_eic_app, z_position=-26.772972, description="BPM02")

# Give the device some inputs.  It has in and out limit switches.
yag_out_lim_sw = models.DeviceInput(channel = digital_chans[0], bit_position = 0, digital_device = screen, fault_value=0)
yag_in_lim_sw = models.DeviceInput(channel = digital_chans[1], bit_position = 1, digital_device = screen, fault_value=0)
gun_temp_channel = models.DeviceInput(channel = digital_chans[2], bit_position = 0,
                                      digital_device = gun_temp, fault_value=0)
wg_temp_channel = models.DeviceInput(channel = digital_chans[3], bit_position = 0, digital_device = wg_temp, fault_value=0)
buncher_temp_channel = models.DeviceInput(channel = digital_chans[4], bit_position = 0,
                                          digital_device = buncher_temp, fault_value=0)
sol01_temp_channel = models.DeviceInput(channel = digital_chans[5], bit_position = 0, 
                                        digital_device = sol01_temp, fault_value=0)
sol02_temp_channel = models.DeviceInput(channel = digital_chans[6], bit_position = 0,
                                        digital_device = sol02_temp, fault_value=0)
vvr1_channel =  models.DeviceInput(channel = digital_chans[7], bit_position = 0,
                                   digital_device = vvr1, fault_value=0)
vvr2_channel =  models.DeviceInput(channel = digital_chans[8], bit_position = 0,
                                   digital_device = vvr2, fault_value=0)

session.add_all([yag_out_lim_sw,yag_in_lim_sw, gun_temp_channel, wg_temp_channel,
                 buncher_temp_channel, sol01_temp_channel, sol02_temp_channel,
                 vvr1_channel, vvr2_channel])

#Configure faults for the digital devices
yag_fault = models.Fault(name="YAG01", description="YAG01 Profile Monitor Fault")
gun_temp_fault = models.Fault(name="GUN_TEMP", description="Gun Temperature Fault")
wg_temp_fault = models.Fault(name="WG_TEMP", description="Waveguide Temperature Fault")
buncher_temp_fault = models.Fault(name="BUNCH_TEMP", description="Buncher Temperature Fault")
sol01_temp_fault = models.Fault(name="SOL01_TEMP", description="SOL01 Temperature Fault")
sol02_temp_fault = models.Fault(name="SOL02_TEMP", description="SOL02 Temperature Fault")
vvr1_fault = models.Fault(name="VVR01", description="VVR01 Vacuum Valve Fault")
vvr2_fault = models.Fault(name="VVR02", description="VVR02 Vacuum Valve Fault")
session.add_all([yag_fault, gun_temp_fault, wg_temp_fault,
                 buncher_temp_fault, sol01_temp_fault, sol02_temp_fault,
                 vvr1_fault, vvr2_fault])

bpm01_fault = models.Fault(name="BPM01", description="BPM01 X/Y/TMIT Threshold Fault")
bpm02_fault = models.Fault(name="BPM02", description="BPM02 X/Y/TMIT Threshold Fault")
session.add_all([bpm01_fault, bpm02_fault])

#bpm01_x_fault = models.Fault(name="BPM01", description="BPM01 X Threshold Fault")
#bpm01_y_fault = models.Fault(name="BPM01", description="BPM01 Y Threshold Fault")
#bpm01_t_fault = models.Fault(name="BPM01", description="BPM01 TMIT Threshold Fault")
#session.add_all([bpm01_x_fault, bpm01_y_fault, bpm01_t_fault])

#bpm02_x_fault = models.Fault(name="BPM01", description="BPM01 X Threshold Fault")
#bpm02_y_fault = models.Fault(name="BPM01", description="BPM01 Y Threshold Fault")
#bpm02_t_fault = models.Fault(name="BPM01", description="BPM01 TMIT Threshold Fault")
#session.add_all([bpm02_x_fault, bpm02_y_fault, bpm02_t_fault])

##### TODO: MAR 24 - review how analog faults/devices are handled. They are more complex than before

# Inputs for the faults
yag_fault_input = models.FaultInput(bit_position = 0, device = screen, fault = yag_fault)
gun_temp_fault_input = models.FaultInput(bit_position = 0, device = gun_temp, fault = gun_temp_fault)
wg_temp_fault_input = models.FaultInput(bit_position = 0, device = wg_temp, fault = wg_temp_fault)
buncher_temp_fault_input = models.FaultInput(bit_position = 0, device = buncher_temp, fault = buncher_temp_fault)
sol01_temp_fault_input = models.FaultInput(bit_position = 0, device = sol01_temp, fault = sol01_temp_fault)
sol02_temp_fault_input = models.FaultInput(bit_position = 0, device = sol02_temp, fault = sol02_temp_fault)
vvr1_fault_input = models.FaultInput(bit_position = 0, device = vvr1, fault = vvr1_fault)
vvr2_fault_input = models.FaultInput(bit_position = 0, device = vvr2, fault = vvr2_fault)
session.add_all([yag_fault_input, gun_temp_fault_input, wg_temp_fault_input,
                 buncher_temp_fault_input, sol01_temp_fault_input, sol02_temp_fault_input,
                 vvr1_fault, vvr2_fault])

bpm01_fault_input = models.FaultInput(bit_position = 0, device = bpm01, fault = bpm01_fault)
bpm02_fault_input = models.FaultInput(bit_position = 0, device = bpm02, fault = bpm02_fault)
session.add_all([bpm01_fault_input, bpm02_fault_input])#

# FaultStates
yag_fault_in = models.FaultState(device_state = screen_in, fault = yag_fault)
yag_fault_moving = models.FaultState(fault = yag_fault, device_state = screen_moving)
yag_fault_broken = models.FaultState(fault = yag_fault, device_state = screen_broken)
gun_temp_fault_state = models.FaultState(fault = gun_temp_fault, device_state = temp_device_fault)
wg_temp_fault_state = models.FaultState(fault = wg_temp_fault, device_state = temp_device_fault)
buncher_temp_fault_state = models.FaultState(fault = buncher_temp_fault, device_state = temp_device_fault)
sol01_temp_fault_state = models.FaultState(fault = sol01_temp_fault, device_state = temp_device_fault)
sol02_temp_fault_state = models.FaultState(fault = sol02_temp_fault, device_state = temp_device_fault)
vvr1_fault_state = models.FaultState(fault = vvr1_fault, device_state = vvr_device_fault)
vvr2_fault_state = models.FaultState(fault = vvr2_fault, device_state = vvr_device_fault)
session.add_all([yag_fault_in, yag_fault_moving, yag_fault_broken,
                 gun_temp_fault_state, wg_temp_fault_state, buncher_temp_fault_state,
                 sol01_temp_fault_state, sol02_temp_fault_state])

# BPM01 threshold fault states - there is one FaultState for each DeviceState,
# there are 24 of them.
bpm01_fault_states=[]
for i in range(0,24):
  bpm01_fault_state = models.FaultState(fault = bpm01_fault, device_state = bpm_states[i])
  session.add(bpm01_fault_state)
  bpm01_fault_states.append(bpm01_fault_state)

# BPM02 threshold fault states - there is one FaultState for each DeviceState,
# there are 24 of them.
bpm02_fault_states=[]
for i in range(0,24):
  bpm02_fault_state = models.FaultState(fault = bpm02_fault, device_state = bpm_states[i])
  session.add(bpm02_fault_state)
  bpm02_fault_states.append(bpm02_fault_state)

# Fault states allowed beam classes.
yag_fault_in.add_allowed_class(beam_class=class_1, mitigation_device=aom)
yag_fault_moving.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
yag_fault_broken.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
gun_temp_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
wg_temp_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
buncher_temp_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
sol01_temp_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
sol02_temp_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
vvr1_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
vvr2_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=shutter)

# Allowed beam classes for the BPM01/BPM02 FaultStates
for fault_state in bpm01_fault_states:
  fault_state.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
  fault_state.add_allowed_class(beam_class=class_0, mitigation_device=aom)

for fault_state in bpm02_fault_states:
  fault_state.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
  fault_state.add_allowed_class(beam_class=class_0, mitigation_device=aom)

# Faults for the analog devices
#fc_fault = models.ThresholdFault(name="FC > 0.1mA", greater_than=True, threshold_value=fc_threshold,
#                                 analog_device = fc)
#fc_fault_state = models.ThresholdFaultState()
#fc_fault_state.add_allowed_class(class_0, mitigation_device=shutter)
#fc_fault.threshold_fault_state = fc_fault_state

#sol01_curr_fault = models.ThresholdFault(name="Curr < 0.05", greater_than=False, threshold_value=sol_threshold,
#                                         analog_device = sol01_curr)
#sol01_curr_fault_state = models.ThresholdFaultState()
#sol01_curr_fault_state.add_allowed_class(class_0, mitigation_device=shutter)
#sol01_curr_fault.threshold_fault_state = sol01_curr_fault_state

#sol02_curr_fault = models.ThresholdFault(name="Curr < 0.05", greater_than=False, threshold_value=sol_threshold,
#                                         analog_device = sol02_curr)
#sol02_curr_fault_state = models.ThresholdFaultState()
#sol02_curr_fault_state.add_allowed_class(class_0, mitigation_device=shutter)
#sol02_curr_fault.threshold_fault_state = sol02_curr_fault_state

# Ignore logic
# 1) If YAG01 is IN, ignore SOL01 Current and SOL02 Current faults, VVR01 and VVR02 faults
yag01_in_condition = models.Condition(name="YAG01_IN", description="YAG01 screen IN", value=0)
session.add(yag01_in_condition)

yag01_condition_input = models.ConditionInput(bit_position=0,fault_state=yag_fault_in,
                                              condition=yag01_in_condition)
session.add(yag01_condition_input)

#sol01_ignore_condition = models.IgnoreCondition(condition=yag01_in_condition, fault_state=sol01_curr_fault_state)
#sol02_ignore_condition = models.IgnoreCondition(condition=yag01_in_condition, fault_state=sol02_curr_fault_state)
vvr1_condition = models.IgnoreCondition(condition=yag01_in_condition, fault_state=vvr1_fault_state)
vvr2_condition = models.IgnoreCondition(condition=yag01_in_condition, fault_state=vvr2_fault_state)
#session.add_all([sol01_ignore_condition, sol02_ignore_condition])
session.add_all([vvr1_condition, vvr2_condition])


session.commit()
