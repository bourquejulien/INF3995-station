import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HistoryPanelComponent } from './history-panel.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('HistoryPanelComponent', () => {
    let component: HistoryPanelComponent;
    let fixture: ComponentFixture<HistoryPanelComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [HistoryPanelComponent],
            providers: [],
            imports: [
                NgbModule,
                HttpClientTestingModule
            ]
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(HistoryPanelComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
