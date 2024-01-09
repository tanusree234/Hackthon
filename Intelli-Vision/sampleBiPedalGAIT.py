import pybullet as p
import time
import pybullet_data
import numpy as np

physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # used by loadURDF
p.setGravity(0, 0, -9.8)
planeId = p.loadURDF("plane.urdf")
humanStartPos = [0, 0, 1]
humanStartOrientation = p.getQuaternionFromEuler([0, 0, 0])
humanId = p.loadURDF(r"C:\Users\tanus\Documents\Github-gl\Hackthon\Intelli-Vision\human-gazebo-master"
                     r"\humanSubject01\humanSubject01_48dof.urdf", humanStartPos, humanStartOrientation)
no_of_joints = p.getNumJoints(humanId)
print(f"No. of Joint: {no_of_joints}")

right_ankle = p.addUserDebugParameter("jRightAnkle")
left_ankle = p.addUserDebugParameter("jLeftAnkle")
right_feet = p.addUserDebugParameter("jRightFeet")
left_feet = p.addUserDebugParameter("jLeftFeet")
right_knee = p.addUserDebugParameter("jRightKnee")
left_knee = p.addUserDebugParameter("jLeftKnee")
right_shoulder = p.addUserDebugParameter("jRightShoulder")
left_shoulder = p.addUserDebugParameter("jLeftShoulder")
left_upper_leg = p.addUserDebugParameter("jLeftUpperLeg")
right_upper_leg = p.addUserDebugParameter("jRightUpperLeg")

for i in range(no_of_joints):
    info = p.getJointInfo(humanId, i)
    print(f"{info[0]}: {info[1]}")
    print("-----------------------------------------")

while True:
    user_right_ankle = p.readUserDebugParameter(right_ankle)
    user_left_ankle = p.readUserDebugParameter(left_ankle)
    user_right_feet = p.readUserDebugParameter(right_feet)
    user_left_feet = p.readUserDebugParameter(left_feet)
    user_left_upper_leg = p.readUserDebugParameter(left_upper_leg)
    user_right_upper_leg = p.readUserDebugParameter(right_upper_leg)
    user_right_knee = p.readUserDebugParameter(right_knee)
    user_left_knee = p.readUserDebugParameter(left_knee)
    user_right_shoulder = p.readUserDebugParameter(right_shoulder)
    user_left_shoulder = p.readUserDebugParameter(left_shoulder)

    p.setJointMotorControl2(humanId, 0, p.POSITION_CONTROL, targetPosition=user_left_ankle)
    p.setJointMotorControl2(humanId, 1, p.POSITION_CONTROL, targetPosition=user_right_ankle)
    p.setJointMotorControl2(humanId, 2, p.POSITION_CONTROL, targetPosition=user_left_feet)
    p.setJointMotorControl2(humanId, 3, p.POSITION_CONTROL, targetPosition=user_right_feet)
    p.setJointMotorControl2(humanId, 4, p.POSITION_CONTROL, targetPosition=user_left_upper_leg)
    p.setJointMotorControl2(humanId, 5, p.POSITION_CONTROL, targetPosition=user_left_knee)
    p.setJointMotorControl2(humanId, 6, p.POSITION_CONTROL, targetPosition=user_right_knee)
    p.setJointMotorControl2(humanId, 7, p.POSITION_CONTROL, targetPosition=user_left_shoulder)
    p.setJointMotorControl2(humanId, 8, p.POSITION_CONTROL, targetPosition=user_right_shoulder)
    p.setJointMotorControl2(humanId, 9, p.POSITION_CONTROL, targetPosition=user_right_upper_leg)

    p.stepSimulation()

'''
'''
for i in range(10000):
    p.stepSimulation()
    time.sleep(1. / 240.)

humanPos, humanOrn = p.getBasePositionAndOrientation(humanId)
print(humanPos, humanOrn)
p.disconnect()
