import { TestBed } from '@angular/core/testing';

import { CommandService } from './command.service';
import { HttpClientModule } from '@angular/common/http';

describe('CommandService', () => {
    let service: CommandService;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [HttpClientModule],
        });
        service = TestBed.inject(CommandService);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });
});
