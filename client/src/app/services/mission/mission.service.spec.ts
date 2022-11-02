import { HttpClientModule } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';

import { MissionService } from './mission.service';

describe('MissionService', () => {
    let service: MissionService;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [HttpClientModule],
        });
        service = TestBed.inject(MissionService);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });
});
