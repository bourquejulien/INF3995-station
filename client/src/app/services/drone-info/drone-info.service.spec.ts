import { TestBed } from '@angular/core/testing';
import { HttpClientModule } from '@angular/common/http';
import { DroneInfoService } from './drone-info.service';

describe('DroneInfoService', () => {
    let service: DroneInfoService;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [HttpClientModule],
        });
        service = TestBed.inject(DroneInfoService);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });
});
