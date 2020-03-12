package my;

import base.Action;
import base.Agent;
import base.Perceptions;
import gridworld.GridOrientation;
import gridworld.GridRelativeOrientation;
import my.MyEnvironment.*;

import java.util.Set;

/**
 * Your implementation of a reactive cleaner agent.
 *
 * @author Andrei Olaru
 */
public class MyAgent implements Agent {
    @Override
    public Action response(Perceptions perceptions, boolean isXEven) {
        MyAgentPerceptions myPerceptions = (MyAgentPerceptions) perceptions;
        Set<GridRelativeOrientation> obstacles = myPerceptions.getObstacles();
        if (myPerceptions.isOverJtile()) {
            return MyAction.PICK;
        }
        switch (myPerceptions.getAbsoluteOrientation()) {
            case NORTH:
                if (obstacles.contains(GridRelativeOrientation.BACK_LEFT) &&
                        !obstacles.contains(GridRelativeOrientation.BACK) &&
                        !obstacles.contains(GridRelativeOrientation.LEFT) && isXEven) {
                    return MyAction.TURN_LEFT;
                }
                if (obstacles.contains(GridRelativeOrientation.FRONT)) {
                    if (obstacles.contains(GridRelativeOrientation.FRONT_LEFT) &&
                            obstacles.contains(GridRelativeOrientation.FRONT_RIGHT)) {
                        return MyAction.TURN_RIGHT;
                    }
                    if (!obstacles.contains(GridRelativeOrientation.RIGHT)) {
                        return MyAction.TURN_RIGHT;
                    }
                    if (!obstacles.contains(GridRelativeOrientation.LEFT)) {
                        return MyAction.TURN_LEFT;
                    }
                }
                break;
            case EAST:
                if (obstacles.contains(GridRelativeOrientation.FRONT) &&
                        obstacles.contains(GridRelativeOrientation.FRONT_RIGHT) &&
                        obstacles.contains(GridRelativeOrientation.FRONT_LEFT)) {
                    if (isXEven) {
                        return MyAction.TURN_RIGHT;
                    } else {
                        return MyAction.FORWARD;
                    }
                }

                if (obstacles.contains(GridRelativeOrientation.BACK) &&
                        obstacles.contains(GridRelativeOrientation.BACK_RIGHT) &&
                        obstacles.contains(GridRelativeOrientation.BACK_LEFT) && !isXEven) {
                    return MyAction.TURN_LEFT;
                }
                if (obstacles.contains(GridRelativeOrientation.FRONT) &&
                        !obstacles.contains(GridRelativeOrientation.FRONT_LEFT) && isXEven) {
                    return MyAction.TURN_RIGHT;
                }
                if (obstacles.contains(GridRelativeOrientation.FRONT_LEFT) &&
                        !obstacles.contains(GridRelativeOrientation.FRONT)) {
                    return MyAction.TURN_LEFT;
                }
                if (obstacles.contains(GridRelativeOrientation.BACK_LEFT) &&
                        !obstacles.contains(GridRelativeOrientation.BACK)) {
                    return MyAction.TURN_RIGHT;
                }
                if (obstacles.contains(GridRelativeOrientation.RIGHT)) {
                    if (!obstacles.contains(GridRelativeOrientation.BACK)) {
                        return MyAction.TURN_RIGHT;
                    }
                    if (!obstacles.contains(GridRelativeOrientation.FRONT)) {
                        return MyAction.TURN_LEFT;
                    }
                }
                break;
            case WEST:
                if (obstacles.contains(GridRelativeOrientation.BACK_RIGHT) &&
                        !obstacles.contains(GridRelativeOrientation.BACK) && !isXEven) {
                    return MyAction.TURN_LEFT;
                }
                if (obstacles.contains(GridRelativeOrientation.BACK) &&
                        !obstacles.contains(GridRelativeOrientation.BACK_RIGHT) && !isXEven) {
                    return MyAction.TURN_RIGHT;
                }
                if (obstacles.contains(GridRelativeOrientation.LEFT)) {
                    if (!obstacles.contains(GridRelativeOrientation.RIGHT)) {
                        return MyAction.TURN_RIGHT;
                    }
                    if (!obstacles.contains(GridRelativeOrientation.BACK)) {
                        return MyAction.TURN_LEFT;
                    }
                }
                break;
            case SOUTH:
                if (obstacles.contains(GridRelativeOrientation.BACK) &&
                        obstacles.contains(GridRelativeOrientation.BACK_LEFT) &&
                        obstacles.contains(GridRelativeOrientation.BACK_RIGHT)) {
                    return MyAction.TURN_LEFT;
                }

                if (obstacles.contains(GridRelativeOrientation.FRONT_RIGHT) &&
                        !obstacles.contains(GridRelativeOrientation.FRONT) && !isXEven) {
                    return MyAction.TURN_LEFT;
                }

                if (obstacles.contains(GridRelativeOrientation.BACK)) {
                    if (!obstacles.contains(GridRelativeOrientation.RIGHT)) {
                        return MyAction.TURN_RIGHT;
                    }
                    if (!obstacles.contains(GridRelativeOrientation.LEFT)) {
                        return MyAction.TURN_LEFT;
                    }
                }
                break;
            default:
                break;
        }

        // TODO Auto-generated method stub
        return MyAction.FORWARD;
    }

    @Override
    public String toString() {
        // TODO Auto-generated method stub
        // please use a single character
        return "1";
    }

}
