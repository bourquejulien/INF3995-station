import { TestBed } from "@angular/core/testing";
import { environment } from "@environment";
import { CommandService } from "./command.service";
import { HttpClientTestingModule, HttpTestingController } from "@angular/common/http/testing";

describe("CommandService", () => {
    let service: CommandService;
    let httpMock: HttpTestingController;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [HttpClientTestingModule],
        });

        httpMock = TestBed.get(HttpTestingController);
        service = TestBed.inject(CommandService);
    });

    afterEach(() => {
        httpMock.verify();
    });

    it("should be created", () => {
        expect(service).toBeTruthy();
    });

    it("should connect", () => {
        const data: [string, boolean][] = [
            ["test1", false],
            ["test2", false],
        ];
        service.connect().then(() => {
            expect(service.uris).toEqual(data);
        });

        const req = httpMock.expectOne(`${environment.serverURL}/discovery/connect`);
        expect(req.request.method).toEqual("POST");
        req.flush(data);
    });

    it("should disconnect", () => {
        service.uris = [
            ["", true],
            ["", true],
        ];

        service.disconnect().then(() => {
            expect(service.uris).toEqual([
                ["", false],
                ["", false],
            ]);
        });

        const req = httpMock.expectOne(`${environment.serverURL}/discovery/disconnect`);
        expect(req.request.method).toEqual("POST");
        req.flush(null);
    });

    it("should identify", () => {
        let mockUris = ["str1", "str2"];

        service.identify({ uris: mockUris });

        const req = httpMock.expectOne(`${environment.serverURL}/action/identify`);
        expect(req.request.method).toEqual("POST");
        req.flush(null);
    });

    it("should toggle sync", () => {
        service.toggleSync();

        const req = httpMock.expectOne(`${environment.serverURL}/action/toggle_sync`);
        expect(req.request.method).toEqual("POST");
        req.flush(null);
    });

    it("should get uris", () => {
        let mockUris: [string, boolean][] = [["0", false]];

        service.getUris().then(() => {
            expect(service.uris).toEqual(mockUris);
        });

        const req = httpMock.expectOne(`${environment.serverURL}/discovery/uris`);
        expect(req.request.method).toEqual("GET");
        req.flush({ "0": false });
    });

    it("should retrieve mode", () => {
        service.isSimulation = false;

        service.retrieveMode().then(() => {
            expect(service.isSimulation).toBeTrue();
        });

        const req = httpMock.expectOne(`${environment.serverURL}/is_simulation`);
        expect(req.request.method).toEqual("GET");
        req.flush(true);
    });
});
