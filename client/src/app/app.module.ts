import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from '@app/component/app/app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from "@angular/common/http";
import { MainPageComponent } from '@app/component/main-page/main-page.component';
import { RouterModule } from '@angular/router';
import { AppRoutingModule } from './app-routing.module';
import { MissionPageComponent } from './component/mission-page/mission-page.component';
import { DronePanelComponent } from '@app/component/drone-panel/drone-panel.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { LogComponent } from '@app/component/log/log.component';
import { MapComponent } from '@app/component/map/map.component';
import { CodeEditorComponent } from './component/code-editor/code-editor.component';
import { FirmwarePanelComponent } from './component/firmware-panel/firmware-panel.component';
import { FormsModule } from '@angular/forms';


@NgModule({
    declarations: [
        AppComponent,
        DronePanelComponent,
        MainPageComponent,
        MissionPageComponent,
        LogComponent,
        MapComponent,
        CodeEditorComponent,
        FirmwarePanelComponent,
    ],
    imports: [
        HttpClientModule,
        BrowserModule,
        BrowserAnimationsModule,
        RouterModule,
        AppRoutingModule,
        NgbModule,
        FormsModule,
    ],
    providers: [],
    bootstrap: [AppComponent],
})
export class AppModule {}
