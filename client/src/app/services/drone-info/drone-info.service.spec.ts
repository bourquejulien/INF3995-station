import { TestBed } from '@angular/core/testing';
import { environment } from '@environment';
import { DroneInfoService } from './drone-info.service';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { Log, Metric } from '@app/interface/commands';
import { MapMetric } from '@app/interface/mapdrone';

describe('DroneInfoService', () => {
    let service: DroneInfoService;
    let httpMock: HttpTestingController;
    let mockMetric: Metric;
    let mockMap: Map<string, MapMetric>;
    let mockLog: Log;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [HttpClientTestingModule],
        });

        httpMock = TestBed.get(HttpTestingController);
        service = TestBed.inject(DroneInfoService);

        mockMetric = {_id: "test", timestamp_ms: 0, position: {x: 0, y: 0, z: 0}, status: "test", drone_uri: "test", mission_id: "test"};  
        mockMap = new Map<string, MapMetric>();
        mockLog = {timestamp_ms: 0, mission_id: "test", message: "test", level: "test"};
    });

    afterEach(() => {
        httpMock.verify();
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });

    it('should get latest metric', () => {
        service.getLatestMetric().subscribe((next) => {
            expect(next).toEqual(mockMetric);
        });

        const req = httpMock.expectOne(`${environment.serverURL}/drone-info/latestMetric`);
        expect(req.request.method).toEqual('GET');
        req.flush(mockMetric);
    });

    it('should get latest map', () => {
        service.getLatestMap().subscribe((next) => {
            expect(next).toEqual(mockMap);
        });

        const req = httpMock.expectOne(`${environment.serverURL}/drone-info/latestMap`);
        expect(req.request.method).toEqual('GET');
        req.flush(mockMap);
    });

    it('should get all metrics', () => {
        let mockMetrics = [mockMetric, mockMetric];

        service.getAllMetrics("test").subscribe((next) => {
            expect(next).toEqual(mockMetrics);
        });

        const req = httpMock.expectOne(`${environment.serverURL}/drone-info/allMetrics?uri=test`);
        expect(req.request.method).toEqual('GET');
        req.flush(mockMetrics);
    });

    it('should get all maps', () => {
        let mockMaps = [mockMap, mockMap];

        service.getAllMapMetric().then(() => {
            expect(service.allMapMetrics).toEqual(new Map(Object.entries(mockMaps)));
        });

        const req = httpMock.expectOne(`${environment.serverURL}/drone-info/maps`);
        expect(req.request.method).toEqual('GET');
        req.flush(mockMaps);
    });

    it('should get logs', () => {
        let mockLogs = [mockLog, mockLog];

        service.getLogs("test", 0).subscribe((next) => {
            expect(next).toEqual(mockLogs);
        });

        const req = httpMock.expectOne(`${environment.serverURL}/drone-info/logs?mission_id=test&since_timestamp=0`);
        expect(req.request.method).toEqual('GET');
        req.flush(mockLogs);
    });
});
