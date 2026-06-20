from setuptools import Distribution, setup

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
except ImportError:  # pragma: no cover
    _bdist_wheel = None


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True

    def is_pure(self):
        return False


cmdclass = {}

if _bdist_wheel is not None:
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(distclass=BinaryDistribution, cmdclass=cmdclass)
