const { expect } = require("chai");

describe("EnvironmentalTrustToken", function () {
  let DeliveryVerification, EnvironmentalTrustToken, deliveryVerification, ett, owner, addr1;

  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();
    DeliveryVerification = await ethers.getContractFactory("DeliveryVerification");
    deliveryVerification = await DeliveryVerification.deploy();
    await deliveryVerification.deployed();

    EnvironmentalTrustToken = await ethers.getContractFactory("EnvironmentalTrustToken");
    ett = await EnvironmentalTrustToken.deploy(deliveryVerification.address);
    await ett.deployed();

    // Add a delivery record for testing ETT minting
    await deliveryVerification.addDeliveryRecord(
      "route_ett_001", "van_001", 12000, 8000, 80000, 93, "hash_ett"
    );
  });

  it("Should mint ETT for a verified delivery", async function () {
    const tx = await ett.createETT(
      "route_ett_001", owner.address, 88, 12000, 92, 0
    );
    await expect(tx).to.emit(ett, "ETTCreated");
    expect(await ett.totalSupply()).to.equal(1);

    const data = await ett.getETTData(1);
    expect(data.routeId).to.equal("route_ett_001");
    expect(data.trustScore).to.equal(88);
    expect(data.isActive).to.equal(true);
  });

  it("Should not mint ETT for unverified delivery", async function () {
    await expect(
      ett.createETT("not_verified", owner.address, 88, 12000, 92, 0)
    ).to.be.revertedWith("Delivery must be verified");
  });

  it("Should allow owner to transfer ETT", async function () {
    await ett.createETT(
      "route_ett_001", owner.address, 88, 12000, 92, 0
    );
    await ett.transferFrom(owner.address, addr1.address, 1);
    expect(await ett.ownerOf(1)).to.equal(addr1.address);
  });

  it("Should not allow non-owner transfer", async function () {
    await ett.createETT(
      "route_ett_001", owner.address, 88, 12000, 92, 0
    );
    await expect(
      ett.connect(addr1).transferFrom(owner.address, addr1.address, 1)
    ).to.be.revertedWith("ERC721: transfer caller is not owner nor approved");
  });

  it("Should allow updating trust score by contract owner", async function () {
    await ett.createETT(
      "route_ett_001", owner.address, 88, 12000, 92, 0
    );
    await ett.updateTrustScore(1, 95);
    const data = await ett.getETTData(1);
    expect(data.trustScore).to.equal(95);
  });
});
