import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
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
    // TODO: communicate with server
    this.router.navigateByUrl("/mission");
  }

  startDrone() : void {
    // TODO: communicate with server
    this.router.navigateByUrl("/mission");
  }


  ngOnInit(): void {
  }

}
