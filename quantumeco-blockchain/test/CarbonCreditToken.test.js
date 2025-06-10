const { expect } = require("chai");

describe("CarbonCreditToken", function () {
  let DeliveryVerification, CarbonCreditToken, deliveryVerification, carbonCredit, owner, addr1;

  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();
    DeliveryVerification = await ethers.getContractFactory("DeliveryVerification");
    deliveryVerification = await DeliveryVerification.deploy();
    await deliveryVerification.deployed();

    CarbonCreditToken = await ethers.getContractFactory("CarbonCreditToken");
    carbonCredit = await CarbonCreditToken.deploy(deliveryVerification.address);
    await carbonCredit.deployed();

    // Add a delivery record for carbon credit issuance
    await deliveryVerification.addDeliveryRecord(
      "route_cc_001", "truck_cc", 35000, 20000, 150000, 91, "hash_cc"
    );
  });

  it("Should issue a carbon credit for a verified delivery", async function () {
    const tx = await carbonCredit.issueCarbonCredit(
      "route_cc_001", 30000, 5000, 5, "QUANTUMECO", 3
    );
    await expect(tx).to.emit(carbonCredit, "CarbonCreditIssued");
    expect(await carbonCredit.getTotalCredits()).to.equal(1);

    const credit = await carbonCredit.getCarbonCredit(1);
    expect(credit.routeId).to.equal("route_cc_001");
    expect(credit.carbonAmount).to.equal(30000);
    expect(credit.quality).to.equal(3);
    expect(credit.isTraded).to.equal(false);
  });

  it("Should not issue carbon credit for unverified delivery", async function () {
    await expect(
      carbonCredit.issueCarbonCredit(
        "nonexistent", 30000, 5000, 5, "QUANTUMECO", 3
      )
    ).to.be.revertedWith("Delivery must be verified");
  });

  it("Should allow retiring a carbon credit", async function () {
    await carbonCredit.issueCarbonCredit(
      "route_cc_001", 30000, 5000, 5, "QUANTUMECO", 3
    );
    await carbonCredit.retireCarbonCredit(1, 10000, "offset");
    const credit = await carbonCredit.getCarbonCredit(1);
    expect(credit.isTraded).to.equal(true);
  });

  it("Should get market statistics", async function () {
    await carbonCredit.issueCarbonCredit(
      "route_cc_001", 30000, 5000, 5, "QUANTUMECO", 3
    );
    const stats = await carbonCredit.getMarketStatistics();
    expect(stats.totalCredits).to.equal(1);
    expect(stats.totalRetired).to.be.a("number");
    expect(stats.totalVolume).to.be.a("number");
  });
});
