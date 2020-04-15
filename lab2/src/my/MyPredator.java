package my;

import base.Action;
import base.Perceptions;
import communication.AgentMessage;
import communication.SocialAction;
import hunting.AbstractWildlifeAgent;
import hunting.WildlifeAgentType;

import communication.AgentID;
import my.MyEnvironment.MyAction;
import gridworld.GridPosition;

import java.util.*;

/**
 * Implementation for predator agents.
 *
 * @author Alexandru Sorici
 */
public class MyPredator extends AbstractWildlifeAgent {
    private MyAction prevAction = null;
    private Set<AgentID> nearbyPredators = new HashSet<AgentID>();

    /**
     * Default constructor.
     */
    public MyPredator() {
        super(WildlifeAgentType.PREDATOR);
    }

    private MyAction getRandomAction() {
        ArrayList<MyAction> array = new ArrayList<>();
		array.add(MyAction.SOUTH);
		array.add(MyAction.EAST);
		array.add(MyAction.NORTH);
        array.add(MyAction.WEST);

        return array.get(new Random().nextInt(array.size()));
    }

	private void getNextAction(GridPosition agentPos, GridPosition nearPrey) {
		int absX = Math.abs(nearPrey.getX() - agentPos.getX());
		int absY = Math.abs(nearPrey.getY() - agentPos.getY());

		if (absX > absY) {
			if (nearPrey.getX() > agentPos.getX()) {
				prevAction = MyAction.EAST;
			} else {
				prevAction = MyAction.WEST;
			}
		} else {
			if (nearPrey.getY() > agentPos.getY()) {
				prevAction = MyAction.NORTH;
			} else {
				prevAction = MyAction.SOUTH;
			}
		}
	}

	private GridPosition getNextGridPosition(MyEnvironment.MyPerceptions myPerceptions) {
		switch (prevAction) {
			case SOUTH:
				return new GridPosition(myPerceptions.getAgentPos().getX(), myPerceptions.getAgentPos().getY() - 1);
			case NORTH:
				return new GridPosition(myPerceptions.getAgentPos().getX(), myPerceptions.getAgentPos().getY() + 1);
			case WEST:
				return new GridPosition(myPerceptions.getAgentPos().getX() - 1, myPerceptions.getAgentPos().getY());
			case EAST:
				return new GridPosition(myPerceptions.getAgentPos().getX() + 1, myPerceptions.getAgentPos().getY());
			default:
				return null;
		}
	}

	private SocialAction getSocialActionFromMessages(MyEnvironment.MyPerceptions myPerceptions, GridPosition agentPos) {
		for (AgentMessage m : myPerceptions.getMessages()) {

			GridPosition nearPrey = (GridPosition) m.getContent();
			if (nearPrey != null) {

				getNextAction(agentPos, nearPrey);

				return new SocialAction(prevAction);
			}
		}
		return null;
	}

	@Override
    public Action response(Perceptions perceptions) {
        // TODO Auto-generated method stub
        MyEnvironment.MyPerceptions myPerceptions = (MyEnvironment.MyPerceptions) perceptions;

		nearbyPredators.addAll(myPerceptions.getNearbyPredators().keySet());

        GridPosition agentPos = myPerceptions.getAgentPos();

        SocialAction socialAction = null;

        GridPosition myPrey = null;

        for (GridPosition nearPrey : myPerceptions.getNearbyPrey()) {

			getNextAction(agentPos, nearPrey);

			socialAction = new SocialAction(prevAction);
            myPrey = nearPrey;
        }

        if (socialAction == null) {
			socialAction = getSocialActionFromMessages(myPerceptions, agentPos);
		}

        GridPosition nextPosition = null;
        if (prevAction != null) {
			nextPosition = getNextGridPosition(myPerceptions);
		}

        if (prevAction == null || myPerceptions.getObstacles().contains(nextPosition)) {
            prevAction = this.getRandomAction();
        }

        if (socialAction == null) {
            socialAction = new SocialAction(prevAction);
        }

        for (AgentID agentId : nearbyPredators) {
            socialAction.addOutgoingMessage(this, agentId, myPrey);
        }

        return socialAction;
    }
}
