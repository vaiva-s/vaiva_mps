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
llrf = models.MitigationDevice(name="RF")
session.add_all([shutter, aom, llrf])

#Make some beam classes.
class_0 = models.BeamClass(number=0,name="Class 0 (0 Hz)")
class_1 = models.BeamClass(number=1,name="Class 1")
class_2 = models.BeamClass(number=2,name="Class 2")
class_3 = models.BeamClass(number=3,name="Class 3")
session.add_all([class_0, class_1, class_2, class_3])

# Make a crate for BPMs, and for the mitigation LN
crate1 = models.Crate(number=1, shelf_number=1, num_slots=6)
crate2 = models.Crate(number=2, shelf_number=1, num_slots=6)
session.add_all([crate1,crate2])

#Define a mixed-mode link node (One digital AMC only)
mixed_link_node_type = models.ApplicationType(name="Mixed Mode Link Node", number=0, digital_channel_count=11, digital_channel_size=1, analog_channel_count=0, analog_channel_size=1)

#Define a mitigation link node (no inputs?)
mitigation_link_node_type = models.ApplicationType(name="Mitigation Link Node", number=2, digital_channel_count=0, digital_channel_size=0, analog_channel_count=0, analog_channel_size=0)

session.add_all([mixed_link_node_type, mitigation_link_node_type])

#Add one application for everything...
global_app = models.Application(global_id=100,name="MyGlobalApp",description="Generic Application")
session.add(global_app)

#Install a mixed-mode link node card in the crate.
link_node_card = models.ApplicationCard(number=1, type=mixed_link_node_type, slot_number = 2)
crate1.cards.append(link_node_card)
session.add(link_node_card)

#Define some channels for the card.
# channel 0 - YAG01 out switch
# channel 1 - YAG01 in switch
# channel 2 - Gun temperature
# channel 3 - Waveguide temperature
# channel 4 - Buncher temperature
# channel 5 - SOL01 temperature
# channel 6 - SOL02 temperature
# channel 7 - SOL01 flow
# channel 8 - SOL02 flow
# channel 9 - VVR01 vacuum status
# channel 10 - VVR02 vacuum status
digital_chans = []
chan_name = ["YAG01_OUT_SWITCH", "YAG01_IN_SWITCH", "GUN_TEMP",
             "WAVEGUIDE_TEMP", "BUNCHER_TEMP", "SOL01_TEMP", "SOL02_TEMP",
             "SOL01_FLOW", "SOL02_FLOW", "VVR01_VAC", "VVR02_VAC"]
for i in range(0,11):
  chan = models.DigitalChannel(number=i)
  chan.name =chan_name[i]
  chan.card = link_node_card
  digital_chans.append(chan)
  session.add(chan)

# Add device types
profmon_device_type = models.DeviceType(name="Profile Monitor")
temp_device_type = models.DeviceType(name="Temperature")
flow_device_type = models.DeviceType(name="Flow Meter")
vvr_device_type = models.DeviceType(name="Vacuum Status")
session.add_all([profmon_device_type, temp_device_type,
                 flow_device_type, vvr_device_type])

# Define some states for the device types
screen_out = models.DeviceState(name="Out", device_type = profmon_device_type, value = 1)
screen_in = models.DeviceState(name="In", device_type = profmon_device_type, value = 2)
screen_moving = models.DeviceState(name="Moving", device_type = profmon_device_type, value = 0)
screen_broken = models.DeviceState(name="Broken", device_type = profmon_device_type, value = 3)
temp_device_fault = models.DeviceState(name="Temperature Fault", device_type = temp_device_type, value = 1)
temp_device_ok = models.DeviceState(name="Temperature OK", device_type = temp_device_type, value = 0)
flow_device_fault = models.DeviceState(name="Flow Fault", device_type = flow_device_type, value = 1)
flow_device_ok = models.DeviceState(name="Flow OK", device_type = flow_device_type, value = 1)
vvr_device_fault = models.DeviceState(name="Vacuum Fault", device_type = vvr_device_type, value = 1)
vvr_device_ok = models.DeviceState(name="Vacuum OK", device_type = vvr_device_type, value = 1)

session.add_all([screen_out, screen_in, screen_moving, screen_broken,
                 temp_device_fault, temp_device_ok,
                 flow_device_fault, flow_device_ok,
                 vvr_device_fault, vvr_device_ok])
session.commit()

#Add the devices
screen = models.DigitalDevice(name="YAG01", z_position=-28.061394, description="YAG Screen",
                              device_type = profmon_device_type, application = global_app)
gun_temp = models.DigitalDevice(name="Gun Temperature", device_type = temp_device_type,
                                application = global_app, z_position = 0,
                                description = "Gun Temperature Summary Input")
wg_temp = models.DigitalDevice(name="Waveguide Temperature", device_type = temp_device_type, 
                               application = global_app, z_position = 0,
                               description = "Waveguide Temperature Summary Input")
buncher_temp = models.DigitalDevice(name="Buncher Temperature", device_type = temp_device_type,
                                    application = global_app, z_position = -30.299721,
                                    description = "Buncher Temperature Summary Input")
sol01_temp = models.DigitalDevice(name="SOL01 Temp", z_position=-32.115049, description="SOL01 Temperature",
                                  device_type = temp_device_type, application = global_app)
sol02_temp = models.DigitalDevice(name="SOL02 Temp", z_position=-27.538278, description="SOL02 Temperature",
                                  device_type = temp_device_type, application = global_app)
sol01_flow = models.DigitalDevice(name="SOL01 Flow", z_position=-32.115049, description="SOL01 Flow",
                                  device_type = flow_device_type, application = global_app)
sol02_flow = models.DigitalDevice(name="SOL02 Flow", z_position=-27.538278, description="SOL02 Flow",
                                  device_type = flow_device_type, application = global_app)
vvr1 = models.DigitalDevice(name="VVR1", z_position=-31, description="Vacuum Gate Valve VVR1",
                                  device_type = vvr_device_type, application = global_app)
vvr2 = models.DigitalDevice(name="VVR2", z_position=-26, description="Vacuum Gate Valve VVR2",
                                  device_type = vvr_device_type, application = global_app)

session.add_all([screen, gun_temp, wg_temp, buncher_temp, sol01_temp, sol02_temp,
                 sol01_flow, sol02_flow, vvr1, vvr2])

# Give the device some inputs.  It has in and out limit switches.
yag_out_lim_sw = models.DeviceInput(channel = digital_chans[0], bit_position = 0, digital_device = screen)
yag_in_lim_sw = models.DeviceInput(channel = digital_chans[1], bit_position = 1, digital_device = screen)
gun_temp_channel = models.DeviceInput(channel = digital_chans[2], bit_position = 0,
                                      digital_device = gun_temp)
wg_temp_channel = models.DeviceInput(channel = digital_chans[3], bit_position = 0, digital_device = wg_temp)
buncher_temp_channel = models.DeviceInput(channel = digital_chans[4], bit_position = 0,
                                          digital_device = buncher_temp)
sol01_temp_channel = models.DeviceInput(channel = digital_chans[5], bit_position = 0, 
                                        digital_device = sol01_temp)
sol02_temp_channel = models.DeviceInput(channel = digital_chans[6], bit_position = 0,
                                        digital_device = sol02_temp)
sol01_flow_channel =  models.DeviceInput(channel = digital_chans[7], bit_position = 0,
                                        digital_device = sol01_flow)
sol02_flow_channel =  models.DeviceInput(channel = digital_chans[8], bit_position = 0,
                                        digital_device = sol02_flow)
vvr1_channel =  models.DeviceInput(channel = digital_chans[9], bit_position = 0,
                                   digital_device = vvr1)
vvr2_channel =  models.DeviceInput(channel = digital_chans[10], bit_position = 0,
                                   digital_device = vvr2)

session.add_all([yag_out_lim_sw,yag_in_lim_sw, gun_temp_channel, wg_temp_channel,
                 buncher_temp_channel, sol01_temp_channel, sol02_temp_channel,
                 sol01_flow_channel, sol02_flow_channel, vvr1_channel, vvr2_channel])

#Configure faults for the device
yag_fault = models.Fault(name="YAG01 Profile Monitor Fault")
gun_temp_fault = models.Fault(name="Gun Temperature Fault")
wg_temp_fault = models.Fault(name="Waveguide Temperature Fault")
buncher_temp_fault = models.Fault(name="Buncher Temperature Fault")
sol01_temp_fault = models.Fault(name="SOL01 Temperature Fault")
sol02_temp_fault = models.Fault(name="SOL02 Temperature Fault")
sol01_flow_fault = models.Fault(name="SOL01 Flow Fault")
sol02_flow_fault = models.Fault(name="SOL02 Flow Fault")
vvr1_fault = models.Fault(name="VVR1 Vacuum Valve Fault")
vvr2_fault = models.Fault(name="VVR2 Vacuum Valve Fault")
session.add_all([yag_fault, gun_temp_fault, wg_temp_fault,
                 buncher_temp_fault, sol01_temp_fault, sol02_temp_fault,
                 sol01_flow_fault, sol02_flow_fault, vvr1_fault, vvr2_fault])

#this fault only has one input: the device state.
yag_fault_input = models.FaultInput(bit_position = 0, device = screen, fault = yag_fault)
gun_temp_fault_input = models.FaultInput(bit_position = 0, device = gun_temp, fault = gun_temp_fault)
wg_temp_fault_input = models.FaultInput(bit_position = 0, device = wg_temp, fault = wg_temp_fault)
buncher_temp_fault_input = models.FaultInput(bit_position = 0, device = buncher_temp, fault = buncher_temp_fault)
sol01_temp_fault_input = models.FaultInput(bit_position = 0, device = sol01_temp, fault = sol01_temp_fault)
sol02_temp_fault_input = models.FaultInput(bit_position = 0, device = sol02_temp, fault = sol02_temp_fault)
session.add_all([yag_fault_input, gun_temp_fault_input, wg_temp_fault_input,
                 buncher_temp_fault_input, sol01_temp_fault_input, sol02_temp_fault_input])

# FaultStates
yag_fault_in = models.DigitalFaultState(device_state = screen_in, fault = yag_fault)
yag_fault_moving = models.DigitalFaultState(fault = yag_fault, device_state = screen_moving)
yag_fault_broken = models.DigitalFaultState(fault = yag_fault, device_state = screen_broken)
gun_temp_fault_state = models.DigitalFaultState(fault = gun_temp_fault, device_state = temp_device_fault)
wg_temp_fault_state = models.DigitalFaultState(fault = wg_temp_fault, device_state = temp_device_fault)
buncher_temp_fault_state = models.DigitalFaultState(fault = buncher_temp_fault, device_state = temp_device_fault)
sol01_temp_fault_state = models.DigitalFaultState(fault = sol01_temp_fault, device_state = temp_device_fault)
sol02_temp_fault_state = models.DigitalFaultState(fault = sol02_temp_fault, device_state = temp_device_fault)
sol01_flow_fault_state = models.DigitalFaultState(fault = sol01_flow_fault, device_state = flow_device_fault)
sol02_flow_fault_state = models.DigitalFaultState(fault = sol02_flow_fault, device_state = flow_device_fault)
vvr1_fault_state = models.DigitalFaultState(fault = vvr1_fault, device_state = vvr_device_fault)
vvr2_fault_state = models.DigitalFaultState(fault = vvr2_fault, device_state = vvr_device_fault)
session.add_all([yag_fault_in, yag_fault_moving, yag_fault_broken,
                 gun_temp_fault_state, wg_temp_fault_state, buncher_temp_fault_state,
                 sol01_temp_fault_state, sol02_temp_fault_state])

# Fault states allowed beam classes.
yag_fault_in.add_allowed_class(beam_class=class_1, mitigation_device=aom)
yag_fault_moving.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
yag_fault_broken.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
gun_temp_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
gun_temp_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=llrf)
wg_temp_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
wg_temp_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=llrf)
buncher_temp_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
buncher_temp_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=llrf)
sol01_temp_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
sol02_temp_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
sol01_flow_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
sol02_flow_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
vvr1_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
vvr1_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=llrf)
vvr2_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=shutter)
vvr2_fault_state.add_allowed_class(beam_class=class_0, mitigation_device=llrf)

session.commit()
