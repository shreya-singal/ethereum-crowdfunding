// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Crowdfunding {
    struct Campaign {
        address payable owner;
        string title;
        uint256 goal;
        uint256 deadline;
        uint256 raised;
        bool withdrawn;
        mapping(address => uint256) contributions;
    }

    uint256 public campaignCount;
    mapping(uint256 => Campaign) public campaigns;

    event CampaignCreated(uint256 id, address indexed owner, string title, uint256 goal, uint256 deadline);
    event Contributed(uint256 indexed id, address indexed contributor, uint256 amount);
    event FundsWithdrawn(uint256 indexed id, uint256 amount);
    event Refunded(uint256 indexed id, address indexed contributor, uint256 amount);

    bool internal locked;

    modifier noReentrant() {
        require(!locked, "No reentrancy");
        locked = true;
        _;
        locked = false;
    }

    modifier campaignExists(uint256 _id) {
        require(_id < campaignCount, "Campaign does not exist");
        _;
    }

    function createCampaign(string memory _title, uint256 _goal, uint256 _duration) public {
        require(bytes(_title).length > 0, "Title is required");
        require(_goal > 0, "Goal must be > 0");
        require(_duration > 0, "Duration must be > 0");

        Campaign storage c = campaigns[campaignCount];
        c.owner = payable(msg.sender);
        c.title = _title;
        c.goal = _goal;
        c.deadline = block.timestamp + _duration;
        c.raised = 0;
        c.withdrawn = false;

        emit CampaignCreated(campaignCount, msg.sender, _title, _goal, c.deadline);
        campaignCount++;
    }

    function contribute(uint256 _id) public payable campaignExists(_id) {
        Campaign storage c = campaigns[_id];
        require(block.timestamp < c.deadline, "Deadline passed");
        require(msg.value > 0, "Must send Ether");

        c.contributions[msg.sender] += msg.value;
        c.raised += msg.value;

        emit Contributed(_id, msg.sender, msg.value);
    }

    function withdrawFunds(uint256 _id) public noReentrant campaignExists(_id) {
        Campaign storage c = campaigns[_id];
        require(msg.sender == c.owner, "Only owner can withdraw");
        require(block.timestamp >= c.deadline, "Deadline not reached");
        require(c.raised >= c.goal, "Goal not met");
        require(!c.withdrawn, "Already withdrawn");

        c.withdrawn = true;
        c.owner.transfer(c.raised);

        emit FundsWithdrawn(_id, c.raised);
    }

    function refund(uint256 _id) public noReentrant campaignExists(_id) {
        Campaign storage c = campaigns[_id];
        require(block.timestamp >= c.deadline, "Deadline not reached");
        require(c.raised < c.goal, "Goal was met");

        uint256 amount = c.contributions[msg.sender];
        require(amount > 0, "Nothing to refund");

        c.contributions[msg.sender] = 0;
        payable(msg.sender).transfer(amount);

        emit Refunded(_id, msg.sender, amount);
    }

    function getCampaign(uint256 _id) public view campaignExists(_id) returns (
        address owner,
        string memory title,
        uint256 goal,
        uint256 deadline,
        uint256 raised,
        bool withdrawn
    ) {
        Campaign storage c = campaigns[_id];
        return (c.owner, c.title, c.goal, c.deadline, c.raised, c.withdrawn);
    }

    function getContribution(uint256 _id, address _addr) public view campaignExists(_id) returns (uint256) {
        return campaigns[_id].contributions[_addr];
    }
}
