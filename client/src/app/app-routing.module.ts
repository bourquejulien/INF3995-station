import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MainPageComponent } from '@app/component/main-page/main-page.component';
import { MissionPageComponent } from './component/mission-page/mission-page.component';

const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: MissionPageComponent },
  { path: 'mission', component: MissionPageComponent },
  { path: '**', redirectTo: '/home' },
];

@NgModule({
  declarations: [],
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],

})
export class AppRoutingModule { }
