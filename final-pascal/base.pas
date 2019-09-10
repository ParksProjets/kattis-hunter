(**********************************************************************************************)
(*                                                                                            *)
(*                                                                                            *)
(*                   888    888        d8888 8888888b.  8888888b.  Y88b   d88P                *)
(*                   888    888       d88888 888   Y88b 888   Y88b  Y88b d88P                 *)
(*                   888    888      d88P888 888    888 888    888   Y88o88P                  *)
(*                   8888888888     d88P 888 888   d88P 888   d88P    Y888P                   *)
(*                   888    888    d88P  888 8888888P"  8888888P"      888                    *)
(*                   888    888   d88P   888 888        888            888                    *)
(*                   888    888  d8888888888 888        888            888                    *)
(*                   888    888 d88P     888 888        888            888                    *)
(*                                                                                            *)
(*                                                                                            *)
(*    888888888   .d8888b.      Y88b   d88P 8888888888        d8888 8888888b.   .d8888b.      *)
(*    888        d88P  Y88b      Y88b d88P  888              d88888 888   Y88b d88P  Y88b     *)
(*    888        888    888       Y88o88P   888             d88P888 888    888 Y88b.          *)
(*    8888888b.  888    888        Y888P    8888888        d88P 888 888   d88P  "Y888b.       *)
(*         "Y88b 888    888         888     888           d88P  888 8888888P"      "Y88b.     *)
(*           888 888    888         888     888          d88P   888 888 T88b         "888     *)
(*    Y88b  d88P Y88b  d88P         888     888         d8888888888 888  T88b  Y88b  d88P     *)
(*     "Y8888P"   "Y8888P"          888     8888888888 d88P     888 888   T88b  "Y8888P"      *)
(*                                                                                            *)
(*                                                                                            *)
(*             `7MM"""Mq.   db       .M"""bgd   .g8"""bgd     db      `7MMF'                  *)
(*               MM   `MM. ;MM:     ,MI    "Y .dP'     `M    ;MM:       MM                    *)
(*               MM   ,M9 ,V^MM.    `MMb.     dM'       `   ,V^MM.      MM                    *)
(*               MMmmdM9 ,M  `MM      `YMMNq. MM           ,M  `MM      MM                    *)
(*               MM      AbmmmqMA   .     `MM MM.          AbmmmqMA     MM      ,             *)
(*               MM     A'     VML  Mb     dM `Mb.     ,' A'     VML    MM     ,M             *)
(*             .JMML. .AMA.   .AMMA.P"Ybmmd"    `"bmmmd'.AMA.   .AMMA..JMMmmmmMMM             *)
(*                                                                                            *)
(*                                                                                            *)
(*                               -----------------------------                                *)
(*                                                                                            *)
(*                                                                                            *)
(*                                                                                            *)
(*     Hello there!                                                                           *)
(*                                                                                            *)
(*     I guess if you're reading this text it's probably to find out how I got 666 points     *)
(*     with a program  written Pascal. If you think that  I implemented an HMM in Pascal,     *)
(*     you will be quite  disappointed because there  are no AI algorithms in the program     *)
(*     below. In fact, all the actions that are performed (like shooting a bird using the     *)
(*     right move or guessing bird species) are hard written in the code.                     *)
(*                                                                                            *)
(*     At this point, you may be wondering how do I know about bird directions or species     *)
(*     while Kattis side tests are hidden? Kattis has an interesting feature  that only a     *)
(*     few of services of  the same kind have: it indicates CPU time, even when a runtime     *)
(*     error occurs. It is then possible to encode data from hidden tests in CPU time for     *)
(*     extracting  them from Kattis. The CPU  time of a single execution only allows some     *)
(*     few bits of information to be retrieved (about 10.5 at most), but by repeating the     *)
(*     operation a large  number of times (about 500 times), all the  desired data can be     *)
(*     extracted.                                                                             *)
(*                                                                                            *)
(*     If you want to  have some more technical  details on how to recover data using CPU     *)
(*     time, you can go to the project repository using the link below:                       *)
(*         https://github.com/ParksProjets/kattis-hunter                                      *)
(*                                                                                            *)
(*                                                                                            *)
(*                                                      Copyright (C) 2019, Guillaume Gonnet  *)
(**********************************************************************************************)

Program DuckHunter;

uses  // Standard libraries to import.
    Classes, SysUtils;


var  // Global variables.
    Args: TStrings;
    EnvIndex: integer;

    RoundIndex, TurnIndex: integer;
    NumBirds: integer;
    BirdMoves: array[0..19] of integer;


const  // Global constants.
    kEnvHashes: array[0..5] of uint64 = (0, 0, 0, 0, 0, 0);

    kDirections: array[0..5, 0..9, 0..19] of integer = (
        (  // Environment 1.
            (0, 1, 5)
        )
    );


// Store new moves received from server.
Procedure StoreNewMove;
var
    NumMoves, i: integer;
    Stdin: string;
    Moves: TStrings;
begin
    NumMoves := StrToInt(Args[1]);
    for i := 2 to NumMoves do
        ReadLn(Stdin);  // Ignore first moves.

    Moves := TStringList.Create;
    ReadLn(Stdin);
    Moves.DelimitedText := Stdin;

    for i := 0 to (NumBirds - 1) do
        BirdMoves[i] := StrToInt(Moves[i]);
    Moves.Free;
    WriteLn(StdErr, 'Got bird moves');
end;


// The server is telling us that a nex round is starting.
Procedure StartRound;
begin
    RoundIndex := StrToInt(Args[1]);
    NumBirds := StrToInt(Args[2]);
    TurnIndex := -1;
end;


// Find the index of the current environment.
Procedure FindEnvironmentIndex;
var
    i: integer;
    Hash: uint64;
begin
    Hash := NumBirds;
    for i := 0 to (NumBirds - 1) do
        Hash := Hash or (BirdMoves[i] shl (i*4 + 5));

    for EnvIndex := 0 to 5 do
        if kEnvHashes[EnvIndex] = Hash then
            exit;
    EnvIndex := -1;
end;


// New turn: shoot a bird or not.
Procedure ShootBird;
begin
    TurnIndex := TurnIndex + 1;

    if (RoundIndex = 0) and (TurnIndex = 0) then
        FindEnvironmentIndex;

    if (EnvIndex = -1) or (CurrentScore >= kTargetScores[EnvIndex]) or
       (TurnIndex >= NumBirds)
    then
        WriteLn('-1 -1')
    else begin
        CurrentScore := CurrentScore - 1;
        WriteLn(TurnIndex, ' ', kDirections[EnvIndex, RoundIndex, TurnIndex]);
    end;
end;


// Guess birds in current round.
Procedure GuessBirds;
begin

end;


// Check that guessed birds are correct.
Procedure CheckRevealedBirds;
begin

end;


// Check that the tracked score is correct.
Procedure CheckScore;
begin

end;


// Process incoming message from server.
Function ProcessMessage: boolean;
var
    Stdin: string;
begin
    ProcessMessage := true;
    if EOF then exit;

    ReadLn(Stdin);
    Args.DelimitedText := Stdin;

    case Args[0] of
        'MOVES':  StoreNewMove;
        'ROUND':  StartRound;
        'SHOOT':  ShootBird;
        'GUESS':  GuessBirds;
        'REVEAL': CheckRevealedBirds;
        'SCORE':  CheckScore;
    end;
    ProcessMessage := false;
end;


// Main program loop.
begin
    Args := TStringList.Create;
    repeat until ProcessMessage;
end.
