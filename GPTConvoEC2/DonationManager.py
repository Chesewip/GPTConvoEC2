from StreamLabsClient import *
import os
from pathlib import Path

class DonationManager:

    def __init__(self):
        self.streamLabs = StreamlabsClient()
        self.donations = self.streamLabs.getDonations()
        self.minDonationAmount = 1.0
        self.lastDonationFilePath = Path.home() / "gptconvo" / "gptconvo" / "LastDonation.txt"

        # Load last donation id
        try:
            with open(self.lastDonationFilePath, "r") as file:
                self.lastDonationId = int(file.read())
        except FileNotFoundError:
            self.lastDonationId = None
    
    def getNextViableDonation(self):
        while not self.donations.empty():
            nextDono = self.donations.get()
            if float(nextDono.amount) >= float(self.minDonationAmount):
                # Save this donation's ID as the last donation ID
                self.lastDonationId = nextDono.id
                with open(self.lastDonationFilePath, "w") as file:
                    file.write(str(self.lastDonationId))
                return nextDono
        return None

    def refreshDonations(self):
        if not self.donations.empty:
            return
        self.donations = self.streamLabs.getDonations(self.lastDonationId);



