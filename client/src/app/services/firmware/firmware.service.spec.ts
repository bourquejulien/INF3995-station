import { TestBed } from '@angular/core/testing';

import { FirmwareService } from './firmware.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { HttpClientModule } from '@angular/common/http';

describe('FirmwareService', () => {
    let service: FirmwareService;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [HttpClientModule],
        });
        service = TestBed.inject(FirmwareService);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });
});
