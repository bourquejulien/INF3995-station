import { Component, OnInit } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { FirmwareService } from '@app/services/firmware/firmware.service';

const DEFAULT_PATH = "main.c";

@Component({
  selector: 'app-code-editor',
  templateUrl: './code-editor.component.html',
  styleUrls: ['./code-editor.component.css']
})
export class CodeEditorComponent implements OnInit {
    filePath: string;
    fileContent: string;
    isPathError: boolean;
    isEditError: boolean;

    constructor(private modalService: NgbModal, private firmwareService: FirmwareService) {
        this.filePath = "";
        this.fileContent = "";
        this.isPathError = false;
        this.isEditError = false;
    }

    ngOnInit(): void {
        this.filePath = DEFAULT_PATH;
        this.fileContent = "";
        this.isPathError = false;
        this.isEditError = false;
    }

    handleKey(event: KeyboardEvent, action: () => void): void {
        if (event.key === "Enter") {
            action()
        }
    }

    getFile(): void {
        this.isPathError = false;

        if (this.filePath === "") {
            return;
        }

        this.firmwareService.getFile(this.filePath).subscribe(
            fileContent => this.fileContent = fileContent,
            err => this.isPathError = true,
        );
    }

    editFile(): void {
        this.isEditError = false;

        if (this.filePath === "" || this.fileContent == "") {
            return;
        }

        this.firmwareService.editFile(this.filePath, this.fileContent).subscribe({
            next: (value: any) => { },
            error: err => console.log(err),
        });
    }

    open(content: any) {
        this.modalService.open(content, { ariaLabelledBy: "Éditeur", size: 'xl' });
    }
}
