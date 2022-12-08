import { Component, OnInit } from "@angular/core";
import { CommandService } from "@app/services/command/command.service";
import { MissionService } from "@app/services/mission/mission.service";

type Pane = "none" | "logs" | "firmware" | "history" | "map-history";

@Component({
    selector: "app-mission-page",
    templateUrl: "./mission-page.component.html",
    styleUrls: ["./mission-page.component.css"],
})
export class MissionPageComponent implements OnInit {
    selectedUris: string[];
    currentMissionId: string;
    currentPane: Pane;
    paneNamesDefault: Array<[Pane, string]>;
    paneNamesFirmware: Array<[Pane, string]>;

    constructor(public commandService: CommandService, public missionService: MissionService) {
        this.selectedUris = [];
        this.currentMissionId = "";
        this.currentPane = "none";
        this.paneNamesDefault = [
            ["logs", "Logs"],
            ["history", "Historique"],
            ["map-history", "Historique Cartes"],
        ];
        this.paneNamesFirmware = [["firmware", "Firmware"]];
    }

    ngOnInit(): void {
        this.commandService.getUris().then(() => {}, this.handleError);
        this.commandService.retrieveMode().then(() => {}, this.handleError);
    }

    isMissionOngoing(): boolean {
        return this.missionService.isMissionOngoing;
    }

    connect(): void {
        this.commandService.connect().then(() => {}, this.handleError);
    }

    disconnect(): void {
        this.commandService.disconnect().then(() => {}, this.handleError);
    }

    identify(): void {
        this.commandService.identify({ uris: this.commandService.uris.map((e) => e[0]) }).then(() => {}, this.handleError);
    }

    toggleSync(): void {
        this.commandService.toggleSync().then(() => {}, this.handleError);
    }

    startMission(): void {
        this.missionService.startMission();
    }

    endMission(): void {
        this.missionService.endMission();
    }

    forceEndMission(): void {
        this.missionService.forceEndMission();
    }

    returnToBase(): void {
        this.missionService.returnToBase();
    }

    togglePane(pane: Pane): void {
        if (this.currentPane == pane) {
            this.currentPane = "none";
            return;
        }
        this.currentPane = pane;
    }

    get paneNames() {
        if (!this.commandService.isSimulation) {
            return this.paneNamesDefault.concat(this.paneNamesFirmware);
        }
        return this.paneNamesDefault;
    }

    handleError(error: Error): void {
        console.log(error);
    }
}
