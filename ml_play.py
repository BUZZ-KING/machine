"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)



def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False
    ball_b_x=[]
    ball_b_y=[]
    ball_x_status=0
    ball_y_status=0
    i=0
    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()
    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        ball_b_x=ball_b_x+[scene_info.ball[0]]
        ball_b_y=ball_b_y+[scene_info.ball[1]]
        if i>2:
            ball_x_status=ball_b_x[i-1]-ball_b_x[i-2]
            ball_y_status=ball_b_y[i-1]-ball_b_y[i-2]
        print("i=",i)
        print("ball_x_status=",ball_x_status)
        print("ball_y_status=",ball_y_status)
        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information
        
        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_RIGHT)
            ball_served = True
        else:
            if ball_y_status<0:
                if scene_info.platform[0]>100:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                elif scene_info.platform[0]<100:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                else:
                     comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            else:
                if ball_x_status>0:
                    if ((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i])<200:
                        print((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i])
                        if (scene_info.platform[0]>(400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i]):
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                        elif (scene_info.platform[0]<(400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i]):
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                        else:
                            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                    if ((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i])>200 and ((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i])<400:
                        print((400-(400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i]))
                        if (scene_info.platform[0]>(400-((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i]))):
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                        elif (scene_info.platform[0]<(400-((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i]))):
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                        else:
                            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                    if ((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i])>400:
                        print(((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i])-400)
                        if (scene_info.platform[0]>((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i])-400):
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                        elif (scene_info.platform[0]<((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i])-400):
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                        else:
                            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                elif ball_x_status<0:
                    if ((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i])>0:
                        print(((400-ball_b_y[i])/ball_y_status*ball_x_status)+ball_b_x[i])
                        if (scene_info.platform[0]>((400-ball_b_y[i])/ball_y_status*ball_x_status)+ball_b_x[i]):
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                        elif (scene_info.platform[0]<((400-ball_b_y[i])/ball_y_status*ball_x_status)+ball_b_x[i]):
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                        else:
                            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                    if ((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i])<0 and ((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i])>-200:
                        print(-((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i]))
                        if scene_info.platform[0]>(-((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i])):
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                        elif scene_info.platform[0]<(-((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i])):
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                        else:
                            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                    if ((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i])<-200:
                        print(((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i])+400)
                        if (scene_info.platform[0]>((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i])+400):
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                        elif (scene_info.platform[0]<((400-ball_b_y[i])/ball_y_status*ball_x_status+ball_b_x[i])+400):
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                        else:
                            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                
                        
        i=i+1

                    
