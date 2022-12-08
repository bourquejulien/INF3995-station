import { environment } from "@environment";
import { HttpClientTestingModule, HttpTestingController } from "@angular/common/http/testing";
import { discardPeriodicTasks, fakeAsync, TestBed, tick } from "@angular/core/testing";
import { MissionService } from "./mission.service";
import { DroneInfoService } from "../drone-info/drone-info.service";
import * as rxjs from "rxjs";
import { Mission } from "@app/interface/commands";

describe("MissionService", () => {
    let service: MissionService;
    let httpMock: HttpTestingController;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [HttpClientTestingModule],
        });

        httpMock = TestBed.get(HttpTestingController);
        service = TestBed.inject(MissionService);
    });

    it("should be created", () => {
        expect(service).toBeTruthy();
    });

    it("should get last missions", () => {
        service["getLastMissions"](0).subscribe();

        const req = httpMock.expectOne(`${environment.serverURL}/mission/?missions_number=0`);
        expect(req.request.method).toEqual("GET");
        req.flush(null);
    });

    it("should get current mission", () => {
        service["getCurrentMission"]().subscribe();

        const req = httpMock.expectOne(`${environment.serverURL}/mission/current_mission`);
        expect(req.request.method).toEqual("GET");
        req.flush(null);
    });

    it("should subscribe to logs", fakeAsync(() => {
        let getLogsSpy = spyOn(service["droneInfoService"], "getLogs").and.returnValue(new rxjs.Observable());
        service["logSubscribe"]("test");
        tick(1000);
        discardPeriodicTasks();

        expect(getLogsSpy).toHaveBeenCalled();
        expect(service["_logSubscription"]).not.toEqual(new rxjs.Subscription());
    }));

    it("should unsubscribe to logs", () => {
        service["_logSubscription"] = new rxjs.Subscription();

        service["logUnsubscribe"]();

        expect(service["_logSubscription"]).not.toEqual(new rxjs.Subscription());
    });

    it("should setup mission", () => {
        let mockMission: Mission = { id: "test", is_simulation: true, total_distance: 0, drone_count: 2, start_time_ms: 0, end_time_ms: 0 };
        let logSubscribeSpy = spyOn<any>(service, "logSubscribe");

        service["setupMission"](mockMission);

        expect(service["_currentLogs"]).toEqual([]);
        expect(service["_currentMission"]).toEqual(mockMission);
        expect(service["_isMissionOngoing"]).toBeTrue();
        expect(logSubscribeSpy).toHaveBeenCalledOnceWith(mockMission.id);
    });

    it("should terminate mission if currentMission is ongoing", () => {
        let mockMission: Mission = { id: "test", is_simulation: true, total_distance: 0, drone_count: 2, start_time_ms: 0, end_time_ms: 0 };
        service["_currentMission"] = mockMission;
        service["_isMissionOngoing"] = true;
        let retrieveMissionsSpy = spyOn(service, "retrieveMissions");
        let logUnsubscribeSpy = spyOn<any>(service, "logUnsubscribe");

        service["terminateMission"]();

        expect(retrieveMissionsSpy).toHaveBeenCalled();
        expect(logUnsubscribeSpy).toHaveBeenCalled();
        expect(service["_isMissionOngoing"]).toBeFalse();
    });

    it("should not terminate mission if currentMission not ongoing", () => {
        service["_isMissionOngoing"] = false;
        let retrieveMissionsSpy = spyOn(service, "retrieveMissions");
        let logUnsubscribeSpy = spyOn<any>(service, "logUnsubscribe");

        service["terminateMission"]();

        expect(retrieveMissionsSpy).not.toHaveBeenCalled();
        expect(logUnsubscribeSpy).not.toHaveBeenCalled();
        expect(service["_isMissionOngoing"]).toBeFalse();
    });

    it("should not start mission if mission is ongoing", () => {
        service["_isMissionOngoing"] = true;
        let setupMissionSpy = spyOn<any>(service, "setupMission");

        service["startMission"]();

        httpMock.expectNone(`${environment.serverURL}/mission/current_mission`);
        expect(setupMissionSpy).not.toHaveBeenCalled();
    });

    it("should start mission if mission is not ongoing", () => {
        service["_isMissionOngoing"] = false;
        let setupMissionSpy = spyOn<any>(service, "setupMission");

        service["startMission"]();

        const req = httpMock.expectOne(`${environment.serverURL}/mission/start`);
        expect(req.request.method).toEqual("POST");
        req.flush(null);

        expect(setupMissionSpy).toHaveBeenCalled();
    });

    it("should not end mission if mission is  not ongoing", () => {
        service["_isMissionOngoing"] = false;
        let terminateMissionSpy = spyOn<any>(service, "terminateMission");

        service["endMission"]();

        httpMock.expectNone(`${environment.serverURL}/mission/end`);
        expect(terminateMissionSpy).not.toHaveBeenCalled();
    });

    it("should end mission if mission is ongoing", () => {
        service["_isMissionOngoing"] = true;
        let terminateMissionSpy = spyOn<any>(service, "terminateMission");

        service["endMission"]();

        const req = httpMock.expectOne(`${environment.serverURL}/mission/end`);
        expect(req.request.method).toEqual("POST");
        req.flush(null);

        expect(terminateMissionSpy).toHaveBeenCalled();
    });

    it("should not force end mission if mission is  not ongoing", () => {
        service["_isMissionOngoing"] = false;
        let terminateMissionSpy = spyOn<any>(service, "terminateMission");

        service["forceEndMission"]();

        httpMock.expectNone(`${environment.serverURL}/mission/force_end`);
        expect(terminateMissionSpy).not.toHaveBeenCalled();
    });

    it("should force end mission if mission is ongoing", () => {
        service["_isMissionOngoing"] = true;
        let terminateMissionSpy = spyOn<any>(service, "terminateMission");

        service["forceEndMission"]();

        const req = httpMock.expectOne(`${environment.serverURL}/mission/force_end`);
        expect(req.request.method).toEqual("POST");
        req.flush(null);

        expect(terminateMissionSpy).toHaveBeenCalled();
    });

    it("should not return to base if mission is  not ongoing", () => {
        service["_isMissionOngoing"] = false;
        let terminateMissionSpy = spyOn<any>(service, "terminateMission");

        service["returnToBase"]();

        httpMock.expectNone(`${environment.serverURL}/mission/return`);
        expect(terminateMissionSpy).not.toHaveBeenCalled();
    });

    it("should return to base if mission is ongoing", () => {
        service["_isMissionOngoing"] = true;
        let terminateMissionSpy = spyOn<any>(service, "terminateMission");

        service["returnToBase"]();

        const req = httpMock.expectOne(`${environment.serverURL}/mission/return`);
        expect(req.request.method).toEqual("POST");
        req.flush(null);

        expect(terminateMissionSpy).toHaveBeenCalled();
    });

    it("should get mission logs", () => {
        let mockMission = {
            mission: { id: "test", is_simulation: true, total_distance: 0, drone_count: 2, start_time_ms: 0, end_time_ms: 0 },
            logs: [],
        };
        service["_missions"] = [mockMission, mockMission, mockMission];
        let getLogsSpy = spyOn<any>(service["droneInfoService"], "getLogs").and.returnValue(new rxjs.Observable());

        service["getMissionLogs"]("test");

        expect(getLogsSpy).toHaveBeenCalled();
    });

    it("should retrieve missions", () => {
        let getLastMissionsSpy = spyOn<any>(service, "getLastMissions").and.returnValue(new rxjs.Observable<Mission[]>());

        service["retrieveMissions"](0);

        expect(getLastMissionsSpy).toHaveBeenCalled();
    });

    it("should return is mission ongoing when calling is mission ongoing", () => {
        service["_isMissionOngoing"] = true;

        let returnValue = service.isMissionOngoing;

        expect(returnValue).toBeTrue();
    });

    it("should return current mission when calling current mission", () => {
        let mockMission: Mission = { id: "test", is_simulation: true, total_distance: 0, drone_count: 2, start_time_ms: 0, end_time_ms: 0 };
        service["_currentMission"] = mockMission;

        let returnValue = service.currentMission;

        expect(returnValue).toEqual(mockMission);
    });

    it("should return missions when calling missions", () => {
        let returnValue = service.missions;

        expect(returnValue).toEqual([]);
    });

    it("should current logs when calling current logs", () => {
        let returnValue = service.currentLogs;

        expect(returnValue).toEqual([]);
    });
});
