import { Component, OnInit } from '@angular/core';
import { ModalDismissReasons, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { FirmwareService } from '@app/services/firmware/firmware.service';

@Component({
  selector: 'app-code-editor',
  templateUrl: './code-editor.component.html',
  styleUrls: ['./code-editor.component.css']
})
export class CodeEditorComponent implements OnInit {
    filePath: string;
    fileContent: string;

    constructor(private modalService: NgbModal, private firmwareService: FirmwareService) {
        this.filePath = "";
        this.fileContent = "";
    }

    ngOnInit(): void {}

    handleKey(event: KeyboardEvent, action: () => void): void {
        if (event.key === "enter") {
            action()
        }
    }

    getFile(): void {
        if (this.filePath === "") {
            return;
        }
        this.firmwareService.getFile(this.filePath).then((content) => this.fileContent = content);
    }

    editFile(): void {
        if (this.filePath === "" || this.fileContent == "") {
            return;
        }
        this.firmwareService.editFile(this.filePath, this.fileContent);
    }

    open(content: any) {
        this.modalService.open(content, { ariaLabelledBy: "Éditeur", size: 'xl' });
    }
}
