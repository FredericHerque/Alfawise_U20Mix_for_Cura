import binascii

from UM.Logger import Logger
from cura.Snapshot import Snapshot
from PyQt5.QtCore import QByteArray, QIODevice, QBuffer

from ..Script import Script


class CreateThumbnailU20Mix(Script):
    def __init__(self):
        super().__init__()

    def _createSnapshot(self, width, height):
        Logger.log("d", "Creating thumbnail image...")
        try:
            return Snapshot.snapshot(width, height)
        except Exception:
            Logger.logException("w", "Failed to create snapshot image")

    def _encodeSnapshot(self, snapshot):
        Logger.log("d", "Encoding thumbnail image...")
        try:
            thumbnail_buffer = QBuffer()
            thumbnail_buffer.open(QBuffer.ReadWrite)
            thumbnail_image = snapshot
            thumbnail_image.save(thumbnail_buffer, "JPG")
            hex_bytes = binascii.hexlify(thumbnail_buffer.data())
            hex_str = hex_bytes.decode("ascii")
            thumbnail_buffer.close()
            return hex_str
        except Exception:
            Logger.logException("w", "Failed to encode snapshot image")

    def _convertSnapshotToGcode(self, encoded_snapshot, width, height, chunk_size=80):
        gcode = []

        encoded_snapshot_length = len(encoded_snapshot)
        gcode.append(";Start printer preprocessing data.Do not change the following data")
        gcode.append(";thumbnail here for U20Mix : Hex encoded 180x180 JPEG, {} octets".format(encoded_snapshot_length))
        gcode.append("W221")

        chunks = ["W220 {}".format(encoded_snapshot[i:i+chunk_size])
                  for i in range(0, len(encoded_snapshot), chunk_size)]
        gcode.extend(chunks)

        gcode.append("W222")
        gcode.append(";End printer preprocessing data")

        return gcode

    def getSettingDataString(self):
        return """{
            "name": "Create Thumbnail for Alfawise U20Mix",
            "key": "CreateThumbnailU20Mix",
            "metadata": {},
            "version": 2,
            "settings":
            {
            }
        }"""

    def execute(self, data):
        width  = 180
        height = 180

        snapshot = self._createSnapshot(width, height)
        if snapshot:
            encoded_snapshot = self._encodeSnapshot(snapshot)
            snapshot_gcode = self._convertSnapshotToGcode(
                encoded_snapshot, width, height)

            for layer in data:
                layer_index = data.index(layer)
                lines = data[layer_index].split("\n")
                for line in lines:
                    if line.startswith(";Generated with Cura"):
                        line_index = lines.index(line)
                        insert_index = line_index + 1
                        lines[insert_index:insert_index] = snapshot_gcode
                        break

                final_lines = "\n".join(lines)
                data[layer_index] = final_lines

        return data
