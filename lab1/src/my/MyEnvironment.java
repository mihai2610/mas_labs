package my;

import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

import base.Action;
import base.Perceptions;
import gridworld.AbstractGridEnvironment;
import gridworld.GridOrientation;
import gridworld.GridPosition;
import gridworld.GridRelativeOrientation;

/**
 * Your implementation of the environment in which cleaner agents work.
 *
 * @author Andrei Olaru
 */
public class MyEnvironment extends AbstractGridEnvironment {
    /**
     * Actions for the cleaner agent.
     *
     * @author Andrei Olaru
     */
    public static enum MyAction implements Action {

        /**
         * The robot must move forward.
         */
        FORWARD,

        /**
         * The robot must turn to the left.
         */
        TURN_LEFT,

        /**
         * The robot must turn to the right.
         */
        TURN_RIGHT,

        /**
         * The robot must clean the current tile.
         */
        PICK,

    }

    /**
     * The perceptions of an agent.
     *
     * @author andreiolaru
     */
    public static class MyAgentPerceptions implements Perceptions {
        /**
         * Obstacles perceived. They are percieved as a relative orientation at which an obstacled is neighbor to the
         * agent. The orientation is relative to the absolute orientation of the agent.
         */
        protected Set<GridRelativeOrientation> obstacles;
        /**
         * <code>true</code> if there is trash in the current tile.
         */
        protected boolean isOverJtile;
        /**
         * The indication of the agent's compass.
         */
        protected GridOrientation absoluteOrientation;

        /**
         * @param obstacleOrientations - Obstacles perceived. They are percieved as a relative orientation at which an obstacled is
         *                             neighbor to the agent. The orientation is relative to the absolute orientation of the agent.
         * @param jTile                - <code>true</code> if there is trash in the current tile.
         * @param orientation          - The indication of the agent's compass.
         */
        public MyAgentPerceptions(Set<GridRelativeOrientation> obstacleOrientations, boolean jTile,
                                  GridOrientation orientation) {
            obstacles = new HashSet<>(obstacleOrientations);
            isOverJtile = jTile;
            absoluteOrientation = orientation;
        }

        /**
         * @return the obstacles, each obstacle perceived as a relative orientation at which the obstacled is neighbor
         * to the agent's current position. The orientation is relative to the absolute orientation of the
         * agent.
         */
        public Set<GridRelativeOrientation> getObstacles() {
            return obstacles;
        }

        /**
         * @return <code>true</code> if there is trash at the agent's current position.
         */
        public boolean isOverJtile() {
            return isOverJtile;
        }

        /**
         * @return the indication of the agent's compass.
         */
        public GridOrientation getAbsoluteOrientation() {
            return absoluteOrientation;
        }

    }

    /**
     * Default constructor. This should call one of the {@link #initialize} methods offered by the super class.
     */
    public MyEnvironment() {
        long seed = System.currentTimeMillis(); // new random experiment
        // long seed = 42L; // existing random experiment
        System.out.println("seed: [" + seed + "]");
        Random rand = new Random(seed);

        super.initialize(10, 10, 10, 5, rand);
    }

    @Override
    public void step() {
        for (GridAgentData agent : getAgentsData()) {
            Set<GridRelativeOrientation> obstacles = new HashSet<GridRelativeOrientation>();
            GridPosition agentPosition = agent.getPosition();
            boolean containsJtiles = getJtiles().contains(agentPosition);

            for (GridRelativeOrientation gridOrientation : GridRelativeOrientation.values()) {
                GridPosition neighbourPosition = agent.getPosition().getNeighborPosition(agent.getOrientation(), gridOrientation);

                if (getXtiles().contains(neighbourPosition)) {
                    obstacles.add(agent.getPosition().getRelativeOrientation(neighbourPosition));
                }
            }

            MyAgentPerceptions agentPerceptions = new MyAgentPerceptions(obstacles, containsJtiles, agent.getOrientation());
            MyAction action = (MyAction) agent.getAgent().response(agentPerceptions, agentPosition.isXEven());
            
            switch (action) {
                case PICK:
                    Jtiles.remove(agentPosition);
                    break;
                case FORWARD:
                    agent.setPosition(agentPosition.getNeighborPosition(agent.getOrientation()));
                    break;
                case TURN_LEFT:
                    switch (agent.getOrientation()) {
                        case EAST:
                            agent.setOrientation(GridOrientation.NORTH);
                            break;
                        case SOUTH:
                            agent.setOrientation(GridOrientation.EAST);
                            break;
                        case WEST:
                            agent.setOrientation(GridOrientation.SOUTH);
                            break;
                        case NORTH:
                            agent.setOrientation(GridOrientation.WEST);
                            break;
                        default:
                            break;
                    }
                    break;
                case TURN_RIGHT:
                    switch (agent.getOrientation()) {
                        case EAST:
                            agent.setOrientation(GridOrientation.SOUTH);
                            break;
                        case SOUTH:
                            agent.setOrientation(GridOrientation.WEST);
                            break;
                        case WEST:
                            agent.setOrientation(GridOrientation.NORTH);
                            break;
                        case NORTH:
                            agent.setOrientation(GridOrientation.EAST);
                            break;
                        default:
                            break;
                    }
                    break;
                default:
                    break;
            }


        }
        // TODO Auto-generated method stub
        // this should iterate through all agents, provide them with perceptions, and apply the
        // action they return.
    }
}
