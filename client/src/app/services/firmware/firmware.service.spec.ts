import { TestBed } from "@angular/core/testing";
import { environment } from "@environment";
import { FirmwareService } from "./firmware.service";
import { HttpClientTestingModule, HttpTestingController } from "@angular/common/http/testing";

describe("FirmwareService", () => {
    let service: FirmwareService;
    let httpMock: HttpTestingController;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [HttpClientTestingModule],
        });

        httpMock = TestBed.get(HttpTestingController);
        service = TestBed.inject(FirmwareService);
    });

    it("should be created", () => {
        expect(service).toBeTruthy();
    });

    it("should build flash", () => {
        service.buildFlash().subscribe();

        const req = httpMock.expectOne(`${environment.serverURL}/firmware/build_flash`);
        expect(req.request.method).toEqual("POST");
        req.flush(null);
    });

    it("should flash file", () => {
        service.flashFile(new File([], "test")).subscribe();

        const req = httpMock.expectOne(`${environment.serverURL}/firmware/flash`);
        expect(req.request.method).toEqual("POST");
        req.flush(null);
    });

    it("should get file", () => {
        service.getFile("test").subscribe();

        const req = httpMock.expectOne(`${environment.serverURL}/firmware/get_file?path=test`);
        expect(req.request.method).toEqual("GET");
        req.flush(null);
    });

    it("should edit file", () => {
        service.editFile("test_path", "test_content").subscribe();

        const req = httpMock.expectOne(`${environment.serverURL}/firmware/edit?path=test_path`);
        expect(req.request.method).toEqual("POST");
        req.flush(null);
    });
});
