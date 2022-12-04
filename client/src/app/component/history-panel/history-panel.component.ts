import { Component, OnInit } from '@angular/core';
import { MissionService } from '@app/services/mission/mission.service';
import { Mission } from '@app/interface/commands';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

const ID_LENGTH = 5;

interface MissionInfo extends Mission {
    total_time: number;
}

type Attribute = keyof MissionInfo;
type AttributeTypes = boolean | number | string;

@Component({
    selector: 'app-history-panel',
    templateUrl: './history-panel.component.html',
    styleUrls: ['./history-panel.component.css'],
})
export class HistoryPanelComponent implements OnInit {
    collapsed: boolean;
    selectedMission: MissionInfo | undefined;
    attributes: Array<[Attribute, string]>;
    currentAttribute: Attribute;

    constructor(private modalService: NgbModal, private readonly missionService: MissionService) {
        this.collapsed = true;
        this.selectedMission = undefined;
        this.attributes = [
            ["id", "Id"],
            ["total_distance", "Distance totale"],
            ["drone_count", "Nb. de drones"],
            ["total_time", "Durée totale"],
            ["start_time_ms", "Heure de début"],
            ["end_time_ms", "Heure de fin"]
        ];
        this.currentAttribute = "start_time_ms";
    }

    ngOnInit(): void {
        this.collapsed = true;
        this.selectedMission = undefined;
        this.currentAttribute = "start_time_ms";
    }

    getAttributeName(attribute: Attribute): string {
        const result = this.attributes.find(e => e[0] === attribute);
        return result == undefined ? "Aucun" : result[1];
    }

    getAttributeAsNumber(mission: MissionInfo, attribute: Attribute): number
    {
        return mission[attribute] as number;
    }

    selectAttribute(attribute: Attribute): void {
        this.currentAttribute = attribute;
        this.collapsed = true;
    }

    isDate(attribute: Attribute): boolean
    {
        const index = ["start_time_ms", "end_time_ms"].findIndex(e => e === attribute);
        return index != -1;
    }

    open(modal: any, mission: MissionInfo) {
        this.selectedMission = mission;
        this.modalService.open(modal, { ariaLabelledBy: "Mission", size: 'l'}).dismissed
            .toPromise()
            .then(() => {
                this.selectedMission = undefined;
            });
    }

    get isHistory(): boolean {
        return this.missionService.missions.length > 0;
    }

    get missions(): Array<MissionInfo> {
        let missions = JSON.parse(JSON.stringify(this.missionService.missions)) as Mission[];
        return missions
            .map(e => {
                const missionInfo: any = e;
                missionInfo.id = e.id.split("-")[0];
                missionInfo.total_time = e.end_time_ms - e.start_time_ms;
                return missionInfo as MissionInfo;
            })
            .sort((a, b) =>
                this.toNumber(b[this.currentAttribute]) -
                this.toNumber(a[this.currentAttribute])
            );
    }

    private toNumber(elem: AttributeTypes): number
    {
        if (typeof elem == "boolean") {
            return elem ? 1 : 0;
        }

        if (typeof elem == "string") {
            let value = 0;
            for (let i = 0; i < elem.length; i++) {
                value += (elem.codePointAt(i) ?? 0) * (elem.length - 1);
            }
            return value;
        }

        return elem
    }
}
