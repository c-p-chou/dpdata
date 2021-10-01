import dpdata.dcdftbmd.output
from dpdata.format import Format

# rotate the system to lammps convention
@Format.register("dcdftbmd")
class VASPOutcarFormat(Format):
    @Format.post("rot_lower_triangular")
    def from_labeled_system(self, file_name, begin=0, step=1, **kwargs):
        data = {}
        data['atom_names'], \
            data['atom_numbs'], \
            data['atom_types'], \
            data['cells'], \
            data['coords'], \
            data['energies'], \
            data['forces'], \
            = dpdata.dcdftbmd.output.get_frames(
                file_name, begin=begin, step=step)
        return data