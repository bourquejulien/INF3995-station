import { HttpClientModule } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CommandService } from '@app/services/command/command.service';

import { MapComponent } from './map.component';
import { BehaviorSubject, Subject } from "rxjs";

describe('MapComponent', () => {
    let component: MapComponent;
    let fixture: ComponentFixture<MapComponent>;
    let mockCommandService: CommandService;

    beforeEach(async () => {
        mockCommandService = jasmine.createSpyObj("CommandService", {"getUris": Promise.resolve(), "retrieveMode": Promise.resolve(),}, {"urisObservable": new Subject<[string, boolean][]>().asObservable() });
        await TestBed.configureTestingModule({
            declarations: [ MapComponent ],
            imports: [HttpClientModule],
            providers: [
                {provide: CommandService, useValue: mockCommandService},
            ]
        })
        .compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(MapComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {

        expect(component).toBeTruthy();
    });
});
