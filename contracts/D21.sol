// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;

import "./IVoteD21.sol";

contract D21 is IVoteD21 {

    address immutable public owner;
    uint private deadline;

    mapping(address => Subject) private subjects;
    mapping(address => Voter) private voters;
    mapping(address => bool) private subjectCreated;
    address[] private subjectsAddr;

    constructor() {
        owner = msg.sender;
        deadline = block.timestamp + 1 weeks;
    }

    // Check we can still vote.
    modifier contractActive {
        require(deadline > block.timestamp, "The elections is now ended.");
        _;
    }

    // Check voter has the right to vote
    modifier voterActive {
        require(voters[msg.sender].canVote, "You can not vote.");
        _;
    }

    // Ensures subject exists
    modifier subjectExist(address addr) {
        require(subjectCreated[addr], "Subject does not exist.");
        _;
    }
    
    function addSubject(string memory name) external contractActive {
        require(!subjectCreated[msg.sender], "One person can create one subject only. You have already created one.");
        subjects[msg.sender] = Subject(name, 0);
        subjectsAddr.push(msg.sender);
        subjectCreated[msg.sender] = true;
    }

    function addVoter(address addr) external contractActive {
        require(msg.sender == owner, "Contract owner only can add voters.");
        require(!voters[addr].canVote, "This person was already added as a voter.");
        voters[addr] = Voter(true, address(0x0), address(0x0), 0);
    }

    function getSubjects() external view returns(address[] memory) {
        return subjectsAddr;
    }

    function getSubject(address addr) external view returns(Subject memory) {
        return subjects[addr];
    }

    function votePositive(address addr) external contractActive voterActive subjectExist(addr) {
        Voter storage vot = voters[msg.sender];
        require(vot.voteCount < 2, "You have already dive positive vote twice.");
        require(vot.votePositiveAddr != addr, "You have already voted for this subject.");
        ++vot.voteCount;
        ++subjects[addr].votes;
        if(vot.voteCount == 1)
            vot.votePositiveAddr = addr;
        else
            vot.votePositiveAddr2 = addr;
    }

    function voteNegative(address addr) external contractActive voterActive subjectExist(addr) {
        Voter storage vot = voters[msg.sender];
        require(vot.voteCount > 1, "You must vote positive twice, before vote negative.");
        require(vot.voteCount < 3, "You have already voted negative.");
        require(vot.votePositiveAddr != addr && vot.votePositiveAddr2 != addr, "You already voted positive for this subject");
        ++vot.voteCount;
        --subjects[addr].votes;
    }

    function getRemainingTime() external contractActive view returns(uint) {
        return deadline - block.timestamp;
    }

    // Results sorted in descending order.
    function getResults() external view returns(Subject[] memory) {
        Subject[] memory subjectArray = new Subject[](subjectsAddr.length);
        for (uint i = 0; i < subjectsAddr.length; i++) {
            subjectArray[i] = subjects[subjectsAddr[i]];
        }
        // quickSort(subjectArray, 0, subjectArray.length - 1);
        return sort_array(subjectArray);
    }

    // Does not work
    // function quickSort(Subject[] memory arr, uint left, uint right) internal pure {
    //     uint i = left;
    //     uint j = right;
    //     if (i == j) return;
    //     int pivot = arr[uint(left + (right - left) / 2)].votes;
    //     while (i <= j) {
    //         while (arr[i].votes > pivot) i++;
    //         while (pivot > arr[j].votes) j--;
    //         if (i <= j) {
    //             (arr[i], arr[j]) = (arr[j], arr[i]);
    //             i++;
    //             j--;
    //         }
    //     }
    //     if (left < j)
    //         quickSort(arr, left, j);
    //     if (i < right)
    //         quickSort(arr, i, right);
    // }

    function sort_array(Subject[] memory arr) private pure returns (Subject[] memory) {
        uint256 l = arr.length;
        for(uint i = 0; i < l; i++) {
            for(uint j = i+1; j < l ;j++) {
                if(arr[i].votes < arr[j].votes) {
                    Subject memory temp = arr[i];
                    arr[i] = arr[j];
                    arr[j] = temp;
                }
            }
        }
        return arr;
    }
}