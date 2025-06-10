const { expect } = require("chai");

describe("DeliveryVerification", function () {
  let DeliveryVerification, deliveryVerification, owner, verifier, addr1;

  beforeEach(async function () {
    [owner, verifier, addr1] = await ethers.getSigners();
    DeliveryVerification = await ethers.getContractFactory("DeliveryVerification");
    deliveryVerification = await DeliveryVerification.deploy();
    await deliveryVerification.deployed();
  });

  it("Should allow adding a delivery record and emit event", async function () {
    const tx = await deliveryVerification.connect(owner).addDeliveryRecord(
      "route_001", "truck_001", 25000, 15000, 100000, 92, "hash_abc"
    );
    await expect(tx).to.emit(deliveryVerification, "DeliveryRecorded")
      .withArgs("route_001", 25000, 15000);
    const record = await deliveryVerification.deliveries("route_001");
    expect(record.verified).to.equal(true);
    expect(record.carbonSaved).to.equal(25000);
  });

  it("Should not allow duplicate delivery records", async function () {
    await deliveryVerification.addDeliveryRecord(
      "route_001", "truck_001", 25000, 15000, 100000, 92, "hash_abc"
    );
    await expect(
      deliveryVerification.addDeliveryRecord(
        "route_001", "truck_002", 30000, 20000, 120000, 95, "hash_def"
      )
    ).to.be.revertedWith("Delivery already verified");
  });

  it("Should require non-empty route and vehicle IDs", async function () {
    await expect(
      deliveryVerification.addDeliveryRecord(
        "", "truck_001", 25000, 15000, 100000, 92, "hash"
      )
    ).to.be.revertedWith("Route ID cannot be empty");
    await expect(
      deliveryVerification.addDeliveryRecord(
        "route_002", "", 25000, 15000, 100000, 92, "hash"
      )
    ).to.be.revertedWith("Vehicle ID cannot be empty");
  });

  it("Should update global statistics", async function () {
    await deliveryVerification.addDeliveryRecord(
      "route_001", "truck_001", 25000, 15000, 100000, 92, "hash_abc"
    );
    expect(await deliveryVerification.totalCarbonSaved()).to.equal(25000);
    expect(await deliveryVerification.totalCostSaved()).to.equal(15000);
    expect(await deliveryVerification.totalDeliveries()).to.equal(1);
  });

  it("Should verify delivery record existence", async function () {
    await deliveryVerification.addDeliveryRecord(
      "route_001", "truck_001", 25000, 15000, 100000, 92, "hash_abc"
    );
    const record = await deliveryVerification.deliveries("route_001");
    expect(record.verified).to.equal(true);
  });

  it("Should allow creating an Environmental Trust Token (ETT)", async function () {
    await deliveryVerification.addDeliveryRecord(
      "route_001", "truck_001", 25000, 15000, 100000, 92, "hash_abc"
    );
    const tx = await deliveryVerification.createETT(
      "route_001", 90, 25000, 95
    );
    await expect(tx).to.emit(deliveryVerification, "ETTCreated")
      .withArgs(1, "route_001", 90);
    const ett = await deliveryVerification.ettTokens(1);
    expect(ett.routeId).to.equal("route_001");
    expect(ett.trustScore).to.equal(90);
    expect(ett.active).to.equal(true);
  });

  it("Should not allow ETT creation for unverified deliveries", async function () {
    await expect(
      deliveryVerification.createETT("nonexistent", 90, 25000, 95)
    ).to.be.revertedWith("Delivery must be verified first");
  });
});
