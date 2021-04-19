"""  Calculation.py

     License:  GNU GENERAL PUBLIC LICENSE Version 3
         Copyright (C) 2020  Uwe Schweinsberg butayama@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.


     A wire frame model of the deformed and healthy femur was generated from 3-D CT images.
     The deformation angles in the coronal and sagittal plane (C and S) and the torsion T were determined
     using "Blender" 3-D modulation software. The formulas and designations used were taken from [1].

     Ein Drahtgittermodell des verformten und gesunden Oberschenkelknochens wurde aus 3-D CT Aufnahmen generiert.
     Die Verformungswinkel in der Coronal- und Sagittalebene ( C und S ) und die Verdrehung T wurden mit Hilfe
     der 3-D Modulationssoftware "Blender" bestimmt. Die verwendeten Formeln und Bezeichnungen wurden [1] entnommen.


     Literatur:
     [1] Sangeorzan BP, Judd RP, Sangeorzan BJ (1989) Mathematical analysis of single-cut osteotomy for complex
     long bone deformity. J Biomech 22(11/12):1271–1278

     [2] Unfallchirurg 1999  ́ 102: 684±690 Springer-Verlag 1999 L. Schweiberer, München
     L. Gürke  · W. Strecker  · S. Martinoli Chirurgische Abteilung, Ospedale Civico, Lugano, Schweiz
     Abteilung für Unfallchirurgie, Hand-, plastische und Wiederherstellungschirurgie, Universitätsklinik Ulm
     Korrektur mehrdimensionaler Deformationen durch eine einzige Osteotomie Graphische Analyse und Operationstechnik
     """

from math import radians, atan2, sqrt, tan, degrees, sin, cos, acos
from ansimarkup import ansiprint
from os import system, getcwd
from os.path import join
import sys
from app.file_handling import text_file_object

class CalculateAngles:

    def copyright_license_popup(self):
        """not used yet"""
        system("gnome-terminal --disable-factory")


    def screen_out(filename, c_a_d, s_a_d, t_a_d, c_a, s_a, t_a, a_tad, a_oa, a_azi, a_ele, a_aor):
        """
        Result output to screen
        :param filename:
        :param c_a_d:
        :param s_a_d:
        :param t_a_d:
        :param c_a:
        :param s_a:
        :param t_a:
        :param a_tad:
        :param a_oa:
        :param a_azi:
        :param a_ele:
        :param a_aor:
        """
        ansiprint(f"""  
        Input Values:
    
        {'coronal_component <red>C</red> [degrees] = ':>50}{c_a_d:6.1f}
        {'sagittal_component <red>S</red> [degrees] = ':>50}{s_a_d:6.1f}
        {'torsion_component <red>T</red> [degrees] = ':>50}{t_a_d:6.1f}
    
        Transformation of degrees in radians
        {'coronal_component C in rad = ':>39}{c_a:8.4f}
        {'sagittal_component S in rad = ':>39}{s_a:8.4f}
        {'torsion_component T in rad = ':>39}{t_a:8.4f}
    
        Calculation according to Sangeorzan, Judd (1989)
        
        {'true angular deformity (15) A = ':>39}{degrees(a_tad):8.1f} degrees ({a_tad:8.4f} rad )
    
        {'orientation angle (16) ':>35}{chr(945)}{'= ':>3}{degrees(a_oa):8.1f} degrees ({a_oa:8.4f} rad )
    
        {'azimuth of vektor k (13) ':>35}{chr(int("3A6", 16))}{'= ':>3}{degrees(a_azi):8.1f} degrees ({a_azi:8.4f} rad )
    
        {'angle of rotation (12) ':>35}{chr(int("398", 16))}{'= ':>3}{degrees(a_ele):8.1f} degrees ({a_ele:8.4f} rad )
    
        {'angle of rotation around k (14) ':>35}{chr(int("3B2", 16))}{'= ':>3}{degrees(a_aor):8.1f} degrees ({a_aor:8.4f} rad )
    
        results are stored in {filename}
    
        """)


    def txt_out(filename, c_a_d, s_a_d, t_a_d, c_a, s_a, t_a, a_tad, a_oa, a_azi, a_ele, a_aor):
        """
        Result output to text file: :param filename:
        :param c_a_d:
        :param s_a_d:
        :param t_a_d:
        :param c_a:
        :param s_a:
        :param t_a:
        :param a_tad:
        :param a_oa:
        :param a_azi:
        :param a_ele:
        :param a_aor:
        """
        path_to_file = join(getcwd(), filename)
        text_file_object(path_to_file)

        with open(filename, 'w') as f_txt:
            sys.stdout = f_txt
            print(f"""  
                Input Values
    
                coronal component  C = {c_a_d:6.1f} degrees
                sagittal component S = {s_a_d:6.1f} degrees
                torsion_component  T = {t_a_d:6.1f} degrees
     
                Transformation of degrees in radians
                coronal component  C  =  {c_a:8.4f}
                sagittal component S  =  {s_a:8.4f}
                torsion component  T  =  {t_a:8.4f}
    
                Calculation according to Sangeorzan, Judd (1989)
    
                true angular deformity (15)
                A = {degrees(a_tad):6.1f} degrees ({a_tad:7.4f} rad )
    
                orientation angle (16)
                {chr(945)} = {degrees(a_oa):6.1f} degrees ({a_oa:7.4f} rad )
    
                azimuth of vektor k (angle between z1 axis and the axis of rotation of vector k ) (13)
                {chr(int("3A6", 16))} = {degrees(a_azi):6.1f} degrees ({a_azi:7.4f} rad )
    
                angle of rotation between x1 axis and the projection of k onto the x1-y1 plane (12)
                {chr(int("398", 16))} = {degrees(a_ele):6.1f} degrees({a_ele:7.4f} rad )
    
                angle of rotation around k (14)
                {chr(int("3B2", 16))} = {degrees(a_aor):6.1f} degrees ({a_aor:7.4f} rad )
    
    
    
                Copyright (C) 2020 | Uwe Schweinsberg | butayama@gmail.com
    
                GNU GENERAL PUBLIC LICENSE Version 3
                This program comes with ABSOLUTELY NO WARRANTY;
                This is free software, and you are welcome to redistribute it
                under certain conditions;  
                For details visit <https://www.gnu.org/licenses/>.
                """)
            sys.stdout = sys.__stdout__


    def calculate(c_a_d=0.0, s_a_d=0.0, t_a_d=0.0):
        """
        Calculation of osteotomy angles according to Sangeorzan, Judd (1989)
        """
        filename = f"result/single_cut_rotational_osteotomy_{c_a_d}" + "_" + f"{s_a_d}" + "_" + f"{t_a_d}" + ".txt"

        c_a = radians(c_a_d)
        s_a = radians(s_a_d)
        t_a = radians(t_a_d)

        h1 = sqrt(tan(c_a) * tan(c_a) + tan(s_a) * tan(s_a))
        a_tad = atan2(h1, 1)
        a_oa = atan2(tan(s_a), tan(c_a))
        a_azi = atan2(-(sin(a_oa) + sin(a_oa - t_a)), (cos(a_oa) + cos(a_oa - t_a)))
        a_ele = atan2(2 * sin(a_tad) * cos(0.5 * t_a), sin(t_a) * (1 + cos(a_tad)))
        a_aor = acos(0.5 * (cos(t_a) + cos(a_tad) + cos(t_a) * cos(a_tad) - 1))
        return filename, c_a_d, s_a_d, t_a_d, c_a, s_a, t_a, a_tad, a_oa, a_azi, a_ele, a_aor


    # if __name__ == "__main__":
    #     filename, c_a_d, s_a_d, t_a_d, c_a, s_a, t_a, a_tad, a_oa, a_azi, a_ele, a_aor = calculate()
    #     screen_out(filename, c_a_d, s_a_d, t_a_d, c_a, s_a, t_a, a_tad, a_oa, a_azi, a_ele, a_aor)
    #     txt_out(filename, c_a_d, s_a_d, t_a_d, c_a, s_a, t_a, a_tad, a_oa, a_azi, a_ele, a_aor)
