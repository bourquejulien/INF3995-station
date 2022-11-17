import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FirmwarePanelComponent } from './firmware-panel.component';

describe('FirmwarePanelComponent', () => {
  let component: FirmwarePanelComponent;
  let fixture: ComponentFixture<FirmwarePanelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FirmwarePanelComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FirmwarePanelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
