// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;

interface IVoteD21{
    
    struct Subject{
        string name;
        int votes;
    }

    struct Voter {
        bool canVote;
        address votePositiveAddr;        
        address votePositiveAddr2;
        uint8 voteCount;
    }
    
    function addSubject(string memory name) external;
    function addVoter(address addr) external;
    function getSubjects() external view returns(address[] memory);
    function getSubject(address addr) external view returns(Subject memory);
    function votePositive(address addr) external;
    function voteNegative(address addr) external;
    function getRemainingTime() external view returns (uint256);
    function getResults() external view returns(Subject[] memory);
}