import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.css']
})
export class MainPageComponent implements OnInit {
  readonly title: string = 'Système aérien d’exploration';

  constructor(private router:Router) {
  }

  startSimulation() : void {
    this.router.navigateByUrl("/mission"); // go to the mission page
  }

  startDrone() : void {
    this.router.navigateByUrl("/mission"); // go to the mission page
  }

  ngOnInit(): void {
  }

}
