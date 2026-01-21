// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Escrow {
    address public buyer;
    address public seller;
    uint256 public amount;

    constructor(address _seller) payable {
        buyer = msg.sender;
        seller = _seller;
        amount = msg.value;
    }

    function release() public {
        require(msg.sender == buyer, "Only buyer");

        uint256 payout = amount;
        amount = 0; // EFFECT first
        payable(seller).transfer(payout);
    }
}
