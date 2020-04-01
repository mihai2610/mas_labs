from typing import List, Dict, Any

from scipy.stats._multivariate import special_ortho_group_frozen

from agents import HouseOwnerAgent, CompanyAgent
from communication import NegotiationMessage


class MyACMEAgent(HouseOwnerAgent):

    def __init__(self, role: str, budget_list: List[Dict[str, Any]]):
        super(MyACMEAgent, self).__init__(role, budget_list)
        self.auction_offer: Dict[str, float] = {}
        self.auction_round: Dict[str, int] = {}

    def propose_item_budget(self, auction_item: str, auction_round: int) -> float:
        self.auction_round[auction_item] = auction_round

        if auction_round is 0:
            self.auction_offer[auction_item] = self.budget_dict[auction_item]/2
            return self.budget_dict[auction_item]/2
        elif auction_round is 1:
            self.auction_offer[auction_item] = self.budget_dict[auction_item]*3/4
            return self.budget_dict[auction_item]*3/4
        else:
            self.auction_offer[auction_item] = self.budget_dict[auction_item]
            return self.budget_dict[auction_item]

    def notify_auction_round_result(self, auction_item: str, auction_round: int, responding_agents: List[str]):
        # print("notify_auction_round_result", auction_item, auction_round, responding_agents)
        pass

    def provide_negotiation_offer(self, negotiation_item: str, partner_agent: str, negotiation_round: int) -> float:

        if self.auction_round[negotiation_item] is 0:
            if negotiation_round is 0:
                return self.auction_offer[negotiation_item] * 4 / 6
            elif negotiation_round is 1:
                return self.auction_offer[negotiation_item] * 5 / 6
            else:
                return self.auction_offer[negotiation_item]

        elif self.auction_round[negotiation_item] is 1:
            if negotiation_round is 0:
                return self.auction_offer[negotiation_item] * 7 / 9
            elif negotiation_round is 1:
                return self.auction_offer[negotiation_item] * 8 / 9
            else:
                return self.auction_offer[negotiation_item]

        else:
            if negotiation_round is 0:
                return self.auction_offer[negotiation_item] * 10 / 12
            elif negotiation_round is 1:
                return self.auction_offer[negotiation_item] * 11 / 12
            else:
                return self.auction_offer[negotiation_item]

    def notify_negotiation_winner(self, negotiation_item: str, winning_agent: str, winning_offer: float) -> None:
        pass


class MyCompanyAgent(CompanyAgent):

    def __init__(self, role: str, specialties: List[Dict[str, Any]]):
        super(MyCompanyAgent, self).__init__(role, specialties)
        self.won_auction = False

    def decide_bid(self, auction_item: str, auction_round: int, item_budget: float) -> bool:
        if auction_item in self.specialties.keys():
            if self.specialties[auction_item] < item_budget:
                return True
        return False

    def notify_won_auction(self, auction_item: str, auction_round: int, num_selected: int):
        self.won_auction = True

    def respond_to_offer(self, initiator_msg: NegotiationMessage) -> float:
        desired_price = self.specialties[initiator_msg.negotiation_item]

        if desired_price <= initiator_msg.offer:
            return initiator_msg.offer

        return (initiator_msg.offer + desired_price)/2

    def notify_contract_assigned(self, construction_item: str, price: float) -> None:
        pass

    def notify_negotiation_lost(self, construction_item: str) -> None:
        pass
