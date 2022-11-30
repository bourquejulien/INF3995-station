import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommandHistoryPanelComponent } from './command-history-panel.component';
import { FirmwarePanelComponent } from '@app/component/firmware-panel/firmware-panel.component';
import { FirmwareService } from '@app/services/firmware/firmware.service';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HttpClient } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('CommandHistoryPanelComponent', () => {
    let component: CommandHistoryPanelComponent;
    let fixture: ComponentFixture<CommandHistoryPanelComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [CommandHistoryPanelComponent],
            providers: [],
            imports: [
                NgbModule,
                HttpClientTestingModule
            ]
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(CommandHistoryPanelComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
