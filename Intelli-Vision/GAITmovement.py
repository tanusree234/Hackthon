import pybullet as pb
import time
import pybullet_data

physicsClient = pb.connect(pb.GUI)
pb.setGravity(0, 0, -9.81)
pb.setAdditionalSearchPath(pybullet_data.getDataPath())
# pb.connect(pb.GUI)

planeId = pb.loadURDF("plane.urdf")
humanStartPos = [0, 0, 1]
humanStartOrientation = pb.getQuaternionFromEuler([0, 0, 0])

# Create a human body model
human_body = pb.loadURDF(r"C:\Users\tanus\Documents\Github-gl\Hackthon\Intelli-Vision\human-gazebo-master"
                         r"\humanSubject01\humanSubject01_48dof.urdf", humanStartPos, humanStartOrientation)

# Define the desired gait pattern
gait_pattern = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]
no_of_joints = pb.getNumJoints(human_body)
print(f"No. of Joint: {no_of_joints}")

right_ankle = pb.addUserDebugParameter("jRightAnkle")
left_ankle = pb.addUserDebugParameter("jLeftAnkle")
right_feet = pb.addUserDebugParameter("jRightFeet")
left_feet = pb.addUserDebugParameter("jLeftFeet")
right_knee = pb.addUserDebugParameter("jRightKnee")
left_knee = pb.addUserDebugParameter("jLeftKnee")
right_shoulder = pb.addUserDebugParameter("jRightShoulder")
left_shoulder = pb.addUserDebugParameter("jLeftShoulder")
left_upper_leg = pb.addUserDebugParameter("jLeftUpperLeg")
right_upper_leg = pb.addUserDebugParameter("jRightUpperLeg")

for i in range(no_of_joints):
    info = pb.getJointInfo(human_body, i)
    print(f"{info[0]}: {info[1]}")
    print("-----------------------------------------")

# Simulate the movement of the human body
for i in range(100):
    # Update the gait pattern
    # gait_pattern[i] = [i, i, i]

    # Set the joint angles of the human body
    # pb.setJointAngles(human_body, gait_pattern)
    user_right_ankle = pb.readUserDebugParameter(right_ankle)
    user_left_ankle = pb.readUserDebugParameter(left_ankle)
    user_right_feet = pb.readUserDebugParameter(right_feet)
    user_left_feet = pb.readUserDebugParameter(left_feet)
    user_left_upper_leg = pb.readUserDebugParameter(left_upper_leg)
    user_right_upper_leg = pb.readUserDebugParameter(right_upper_leg)
    user_right_knee = pb.readUserDebugParameter(right_knee)
    user_left_knee = pb.readUserDebugParameter(left_knee)
    user_right_shoulder = pb.readUserDebugParameter(right_shoulder)
    user_left_shoulder = pb.readUserDebugParameter(left_shoulder)

    pb.setJointMotorControl2(human_body, 0, pb.POSITION_CONTROL, targetPosition=user_left_ankle)
    pb.setJointMotorControl2(human_body, 1, pb.POSITION_CONTROL, targetPosition=user_right_ankle)
    pb.setJointMotorControl2(human_body, 2, pb.POSITION_CONTROL, targetPosition=user_left_feet)
    pb.setJointMotorControl2(human_body, 3, pb.POSITION_CONTROL, targetPosition=user_right_feet)
    pb.setJointMotorControl2(human_body, 4, pb.POSITION_CONTROL, targetPosition=user_left_upper_leg)
    pb.setJointMotorControl2(human_body, 5, pb.POSITION_CONTROL, targetPosition=user_left_knee)
    pb.setJointMotorControl2(human_body, 6, pb.POSITION_CONTROL, targetPosition=user_right_knee)
    pb.setJointMotorControl2(human_body, 7, pb.POSITION_CONTROL, targetPosition=user_left_shoulder)
    pb.setJointMotorControl2(human_body, 8, pb.POSITION_CONTROL, targetPosition=user_right_shoulder)
    pb.setJointMotorControl2(human_body, 9, pb.POSITION_CONTROL, targetPosition=user_right_upper_leg)
    pb.stepSimulation()

    # Wait for a short time
    time.sleep(10)
humanPos, humanOrn = pb.getBasePositionAndOrientation(human_body)
print(humanPos, humanOrn)
pb.disconnect()
